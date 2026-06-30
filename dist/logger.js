// ---- Log Levels ----
export var LogLevel;
(function (LogLevel) {
    LogLevel[LogLevel["DEBUG"] = 0] = "DEBUG";
    LogLevel[LogLevel["INFO"] = 1] = "INFO";
    LogLevel[LogLevel["WARN"] = 2] = "WARN";
    LogLevel[LogLevel["ERROR"] = 3] = "ERROR";
    LogLevel[LogLevel["NONE"] = 4] = "NONE";
})(LogLevel || (LogLevel = {}));
const LOG_LEVEL_NAMES = {
    [LogLevel.DEBUG]: 'DEBUG',
    [LogLevel.INFO]: 'INFO',
    [LogLevel.WARN]: 'WARN',
    [LogLevel.ERROR]: 'ERROR',
    [LogLevel.NONE]: 'NONE',
};
// ---- Logger ----
export class Logger {
    level;
    constructor(level = LogLevel.INFO) {
        this.level = level;
    }
    setLevel(level) {
        this.level = level;
    }
    formatTimestamp() {
        return new Date().toISOString().replace('T', ' ').slice(0, 19);
    }
    shouldLog(level) {
        return level >= this.level;
    }
    debug(...args) {
        if (!this.shouldLog(LogLevel.DEBUG))
            return;
        console.debug(`\x1b[90m[${this.formatTimestamp()}] [DEBUG]\x1b[0m`, ...args);
    }
    info(...args) {
        if (!this.shouldLog(LogLevel.INFO))
            return;
        console.info(`\x1b[36m[${this.formatTimestamp()}] [INFO]\x1b[0m`, ...args);
    }
    warn(...args) {
        if (!this.shouldLog(LogLevel.WARN))
            return;
        console.warn(`\x1b[33m[${this.formatTimestamp()}] [WARN]\x1b[0m`, ...args);
    }
    error(...args) {
        if (!this.shouldLog(LogLevel.ERROR))
            return;
        console.error(`\x1b[31m[${this.formatTimestamp()}] [ERROR]\x1b[0m`, ...args);
    }
    /** Log an LLM API call */
    llmCall(model, messageCount, toolCount) {
        this.info(`\x1b[35m[LLM]\x1b[0m model=${model} messages=${messageCount} tools=${toolCount}`);
    }
    /** Log a tool invocation */
    toolCall(toolName, args) {
        this.info(`\x1b[33m[TOOL]\x1b[0m \x1b[93m${toolName}\x1b[0m args=${JSON.stringify(args)}`);
    }
    /** Log a tool execution result */
    toolResult(toolName, result) {
        this.debug(`\x1b[33m[TOOL_RESULT]\x1b[0m \x1b[93m${toolName}\x1b[0m result=${result.slice(0, 200)}${result.length > 200 ? '...' : ''}`);
    }
    /** Log the final assistant response */
    response(content) {
        this.info(`\x1b[32m[RESPONSE]\x1b[0m ${content.slice(0, 500)}${content.length > 500 ? '...' : ''}`);
    }
    /** Print a separator line */
    separator() {
        console.log('\x1b[90m' + '─'.repeat(50) + '\x1b[0m');
    }
}
// ---- Singleton Instance ----
export const logger = new Logger(process.env.LOG_LEVEL !== undefined
    ? LogLevel[process.env.LOG_LEVEL] ?? LogLevel.INFO
    : LogLevel.INFO);
//# sourceMappingURL=logger.js.map