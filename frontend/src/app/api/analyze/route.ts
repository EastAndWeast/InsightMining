import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(req: Request) {
    try {
        const { url, platform } = await req.json();
        console.log(`[API] Starting analysis for ${platform} at ${url}`);

        const projectRoot = path.resolve(process.cwd(), '..');
        const bridgeScript = path.join(projectRoot, 'scripts', 'bridge_analyze.py');

        console.log(`[API] Spawning Python: ${bridgeScript} inside ${projectRoot}`);

        const analysisResult = await new Promise((resolve, reject) => {
            // Windows下强制Python使用UTF-8编码输出
            const pythonProcess = spawn('python', [bridgeScript], {
                cwd: projectRoot,
                env: {
                    ...process.env,
                    PYTHONPATH: projectRoot,
                    PYTHONIOENCODING: 'utf-8',
                    PYTHONUTF8: '1'
                }
            });

            const stdoutChunks: Buffer[] = [];
            const stderrChunks: Buffer[] = [];

            // 透传 URL 和 Platform，触发真实抓取
            pythonProcess.stdin.write(JSON.stringify({ url, platform }));
            pythonProcess.stdin.end();

            pythonProcess.stdout.on('data', (data: Buffer) => {
                stdoutChunks.push(data);
                console.log(`[Python Stdout Chunk]: ${data.toString('utf-8').substring(0, 50)}...`);
            });

            pythonProcess.stderr.on('data', (data: Buffer) => {
                stderrChunks.push(data);
                console.error(`[Python Stderr Chunk]: ${data.toString('utf-8')}`);
            });

            pythonProcess.on('close', (code) => {
                // 合并Buffer chunks并解码为UTF-8字符串
                const stdoutData = Buffer.concat(stdoutChunks).toString('utf-8');
                const stderrData = Buffer.concat(stderrChunks).toString('utf-8');

                console.log(`[API] Python process closed with code ${code}`);
                if (code !== 0) {
                    reject(new Error(`Python Error: ${stderrData || 'Process failed without output'}`));
                    return;
                }
                try {
                    const jsonMatch = stdoutData.match(/\{[\s\S]*\}/);
                    if (jsonMatch) {
                        resolve(JSON.parse(jsonMatch[0]));
                    } else {
                        reject(new Error(`No valid JSON found in output: ${stdoutData.substring(0, 100)}`));
                    }
                } catch (e) {
                    reject(new Error(`Parse Fail: ${stdoutData.substring(0, 100)}`));
                }
            });
        });

        return NextResponse.json(analysisResult);
    } catch (error: any) {
        console.error('[API Error Detail]:', error);
        return NextResponse.json({ error: error.message || 'Internal server error' }, { status: 500 });
    }
}
