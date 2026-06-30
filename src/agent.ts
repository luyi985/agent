import OpenAI from 'openai';
import { logger } from './logger.js';

// ---- Types ----

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  execute: (args: Record<string, unknown>) => Promise<string>;
}

export interface AgentConfig {
  baseURL: string;
  apiKey: string;
  model: string;
  systemPrompt?: string;
}

// ---- Agent ----

export class Agent {
  private client: OpenAI;
  private model: string;
  private tools: Tool[] = [];
  private messages: OpenAI.Chat.Completions.ChatCompletionMessageParam[] = [];

  constructor(config: AgentConfig) {
    this.client = new OpenAI({
      baseURL: config.baseURL,
      apiKey: config.apiKey,
    });
    this.model = config.model;
   // log configuration
   logger.info(`Agent initialized with model: ${this.model}`);
   logger.info(`Base URL: ${config.baseURL}`);
   logger.info(`API Key: ${config.apiKey ?? 'None'}`);

    if (config.systemPrompt) {
      this.messages.push({ role: 'system', content: config.systemPrompt });
    }
  }

  /** Register a tool that the agent can invoke */
  registerTool(tool: Tool): void {
    this.tools.push(tool);
    logger.info(`Tool registered: ${tool.name}`);
  }

  /** Add a user message and run the agent loop */
  async run(userInput: string): Promise<string> {
    this.messages.push({ role: 'user', content: userInput });
    return this.loop();
  }

  private async loop(): Promise<string> {
    const toolDefinitions = this.tools.map(
      (t) =>
        ({
          type: 'function' as const,
          function: {
            name: t.name,
            description: t.description,
            parameters: t.parameters,
          },
        }) satisfies OpenAI.ChatCompletionTool,
    );

    // eslint-disable-next-line no-constant-condition
    while (true) {
      const params: OpenAI.ChatCompletionCreateParamsNonStreaming = {
        model: this.model,
        messages: this.messages,
      };
      if (toolDefinitions.length > 0) {
        params.tools = toolDefinitions;
        params.tool_choice = 'auto';
      }

      logger.llmCall(this.model, this.messages.length, toolDefinitions.length);
      const response = await this.client.chat.completions.create(params);

      const message = response.choices[0]?.message;
      logger.debug('[RAW_RESPONSE]', message);
      if (!message) throw new Error('No response from LLM');

      // Push assistant message (may include tool_calls)
      this.messages.push(message);

      // If no tool calls, return the content
      if (!message.tool_calls || message.tool_calls.length === 0) {
        const content = message.content ?? '';
        logger.response(content);
        return content;
      }

      // Execute each tool call
      for (const toolCall of message.tool_calls) {
        if (toolCall.type !== 'function') {
          this.messages.push({
            role: 'tool',
            tool_call_id: toolCall.id,
            content: `Unsupported tool call type: ${toolCall.type}`,
          });
          continue;
        }

        logger.toolCall(toolCall.function.name, JSON.parse(toolCall.function.arguments));

        const tool = this.tools.find(
          (t) => t.name === toolCall.function.name,
        );
        if (!tool) {
          this.messages.push({
            role: 'tool',
            tool_call_id: toolCall.id,
            content: `Unknown tool: ${toolCall.function.name}`,
          });
          continue;
        }

        let args: Record<string, unknown>;
        try {
          args = JSON.parse(toolCall.function.arguments);
        } catch {
          args = {};
        }

        const result = await tool.execute(args);
        logger.toolResult(tool.name, result);
        this.messages.push({
          role: 'tool',
          tool_call_id: toolCall.id,
          content: result,
        });
      }
    }
  }
}