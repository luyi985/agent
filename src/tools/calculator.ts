import type { Tool } from "../agent.js";

export const calculatorTool: Tool = {
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