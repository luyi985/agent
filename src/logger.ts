// ---- Log Levels ----

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
  NONE = 4,
}

const LOG_LEVEL_NAMES: Record<LogLevel, string> = {
  [LogLevel.DEBUG]: 'DEBUG',
  [LogLevel.INFO]: 'INFO',
  [LogLevel.WARN]: 'WARN',
  [LogLevel.ERROR]: 'ERROR',
  [LogLevel.NONE]: 'NONE',
};

// ---- Logger ----

export class Logger {
  private level: LogLevel;

  constructor(level: LogLevel = LogLevel.INFO) {
    this.level = level;
  }

  setLevel(level: LogLevel): void {
    this.level = level;
  }

  private formatTimestamp(): string {
    return new Date().toISOString().replace('T', ' ').slice(0, 19);
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.level;
  }

  debug(...args: unknown[]): void {
    if (!this.shouldLog(LogLevel.DEBUG)) return;
    console.debug(`\x1b[90m[${this.formatTimestamp()}] [DEBUG]\x1b[0m`, ...args);
  }

  info(...args: unknown[]): void {
    if (!this.shouldLog(LogLevel.INFO)) return;
    console.info(`\x1b[36m[${this.formatTimestamp()}] [INFO]\x1b[0m`, ...args);
  }

  warn(...args: unknown[]): void {
    if (!this.shouldLog(LogLevel.WARN)) return;
    console.warn(`\x1b[33m[${this.formatTimestamp()}] [WARN]\x1b[0m`, ...args);
  }

  error(...args: unknown[]): void {
    if (!this.shouldLog(LogLevel.ERROR)) return;
    console.error(`\x1b[31m[${this.formatTimestamp()}] [ERROR]\x1b[0m`, ...args);
  }

  /** Log an LLM API call */
  llmCall(model: string, messageCount: number, toolCount: number): void {
    this.info(
      `\x1b[35m[LLM]\x1b[0m model=${model} messages=${messageCount} tools=${toolCount}`,
    );
  }

  /** Log a tool invocation */
  toolCall(toolName: string, args: Record<string, unknown>): void {
    this.info(
      `\x1b[33m[TOOL]\x1b[0m \x1b[93m${toolName}\x1b[0m args=${JSON.stringify(args)}`,
    );
  }

  /** Log a tool execution result */
  toolResult(toolName: string, result: string): void {
    this.debug(
      `\x1b[33m[TOOL_RESULT]\x1b[0m \x1b[93m${toolName}\x1b[0m result=${result.slice(0, 200)}${result.length > 200 ? '...' : ''}`,
    );
  }

  /** Log the final assistant response */
  response(content: string): void {
    this.info(
      `\x1b[32m[RESPONSE]\x1b[0m ${content.slice(0, 500)}${content.length > 500 ? '...' : ''}`,
    );
  }

  /** Print a separator line */
  separator(): void {
    console.log('\x1b[90m' + '─'.repeat(50) + '\x1b[0m');
  }
}

// ---- Singleton Instance ----

export const logger = new Logger(
  (process.env.LOG_LEVEL as keyof typeof LogLevel) !== undefined
    ? LogLevel[process.env.LOG_LEVEL as keyof typeof LogLevel] ?? LogLevel.INFO
    : LogLevel.INFO,
);