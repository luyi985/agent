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
export declare class Agent {
    private client;
    private model;
    private tools;
    private messages;
    constructor(config: AgentConfig);
    /** Register a tool that the agent can invoke */
    registerTool(tool: Tool): void;
    /** Add a user message and run the agent loop */
    run(userInput: string): Promise<string>;
    private loop;
}
//# sourceMappingURL=agent.d.ts.map