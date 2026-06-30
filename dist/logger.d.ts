export declare enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3,
    NONE = 4
}
export declare class Logger {
    private level;
    constructor(level?: LogLevel);
    setLevel(level: LogLevel): void;
    private formatTimestamp;
    private shouldLog;
    debug(...args: unknown[]): void;
    info(...args: unknown[]): void;
    warn(...args: unknown[]): void;
    error(...args: unknown[]): void;
    /** Log an LLM API call */
    llmCall(model: string, messageCount: number, toolCount: number): void;
    /** Log a tool invocation */
    toolCall(toolName: string, args: Record<string, unknown>): void;
    /** Log a tool execution result */
    toolResult(toolName: string, result: string): void;
    /** Log the final assistant response */
    response(content: string): void;
    /** Print a separator line */
    separator(): void;
}
export declare const logger: Logger;
//# sourceMappingURL=logger.d.ts.map