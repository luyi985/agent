import { config } from 'dotenv';
import { expand } from 'dotenv-expand';
import { Agent, type Tool } from './agent.js';
import { timeTool } from './tools/time.js';
import { calculatorTool } from './tools/calculator.js';

expand(config());
// ---- Main ----
async function main() {
  const baseURL = process.env.OPENAI_BASE_URL;
  const apiKey = process.env.OPENAI_API_KEY;
  const model = process.env.OPENAI_MODEL;

  if (!baseURL || !apiKey || !model) {
    console.error(
      'Missing environment variables. Please set OPENAI_BASE_URL, OPENAI_API_KEY, and OPENAI_MODEL in .env',
    );
    process.exit(1);
  }

  const agent = new Agent({
    baseURL,
    apiKey,
    model,
    systemPrompt:
      'You are a helpful AI assistant with access to tools. Use them when needed to answer the user\'s questions accurately.',
  });

  agent.registerTool(timeTool);
  agent.registerTool(calculatorTool);

  // Interactive CLI
  const args = process.argv.slice(2);
  if (args.length > 0) {
    // Single query mode
    const query = args.join(' ');
    console.log(`\n🤖 Query: ${query}\n`);
    const response = await agent.run(query);
    console.log(`📝 Response:\n${response}\n`);
  } else {
    // Interactive mode
    console.log('\n🤖 LLM Agent - Interactive Mode');
    console.log('Type "exit" or "quit" to stop.\n');

    const readline = (await import('readline')).default;
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    const ask = () => {
      rl.question('You: ', async (input) => {
        if (input.toLowerCase() === 'exit' || input.toLowerCase() === 'quit') {
          console.log('Goodbye!');
          rl.close();
          return;
        }

        try {
          const response = await agent.run(input);
          console.log(`\nAgent: ${response}\n`);
        } catch (err) {
          console.error(`\nError: ${err}\n`);
        }

        ask();
      });
    };

    ask();
  }
}

main().catch(console.error);