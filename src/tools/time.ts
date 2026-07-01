import type { Tool } from "../agent.js";

export const timeTool: Tool = {
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