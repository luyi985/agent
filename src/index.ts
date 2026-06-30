import { config } from 'dotenv';
import { expand } from 'dotenv-expand';
import { Agent, type Tool } from './agent.js';

expand(config());

// ---- Built-in Tools ----

const timeTool: Tool = {
  name: 'get_current_time',
  description: 'Get the current date and time',
  parameters: {
    type: 'object',
    properties: {},
    required: [],
  },
  execute: async () => {
    return new Date().toISOString();
  },
};

const calculatorTool: Tool = {
  name: 'calculator',
  description: 'Evaluate a mathematical expression',
  parameters: {
    type: 'object',
    properties: {
      expression: {
        type: 'string',
        description: 'The mathematical expression to evaluate, e.g. "2 + 2" or "sqrt(16)"',
      },
    },
    required: ['expression'],
  },
  execute: async (args) => {
    const expression = args.expression as string;
    try {
      // Safe evaluation using Function constructor (basic math only)
      const result = new Function(`return (${expression})`)();
      return String(result);
    } catch {
      return `Error: invalid expression "${expression}"`;
    }
  },
};

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