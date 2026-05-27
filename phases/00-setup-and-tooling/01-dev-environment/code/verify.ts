import { execSync } from "child_process";

interface Check {
  name: string;
  fn: () => string | boolean;
}

function cmd(command: string): string {
  return execSync(command, { encoding: "utf8" }).trim();
}

function nodeVersion(): number {
  return parseInt(process.version.replace("v", "").split(".")[0], 10);
}

const CHECKS: Check[] = [
  {
    name: "Node.js 20+",
    fn: () => {
      const v = nodeVersion();
      if (v < 20) throw new Error(`Node ${process.version} is too old`);
      return process.version;
    },
  },
  {
    name: "npm",
    fn: () => cmd("npm --version"),
  },
  {
    name: "TypeScript (tsc)",
    fn: () => {
      try {
        return cmd("tsc --version");
      } catch {
        throw new Error("not found — run: npm install -g typescript");
      }
    },
  },
  {
    name: "tsx",
    fn: () => {
      try {
        return cmd("npx tsx --version");
      } catch {
        throw new Error("not found — run: npm install -g tsx");
      }
    },
  },
  {
    name: "Git",
    fn: () => cmd("git --version"),
  },
  {
    name: "Python 3.11+",
    fn: () => {
      const out = cmd("python3 --version");
      const minor = parseInt(out.split(".")[1], 10);
      if (minor < 11) throw new Error(`${out} is too old`);
      return out;
    },
  },
  {
    name: "uv",
    fn: () => cmd("uv --version"),
  },
  {
    name: "Rust (cargo)",
    fn: () => cmd("cargo --version"),
  },
];

function runCheck(check: Check): boolean {
  try {
    const detail = check.fn();
    console.log(`  [PASS] ${check.name}${detail ? ` (${detail})` : ""}`);
    return true;
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : String(e);
    console.log(`  [FAIL] ${check.name} — ${msg}`);
    return false;
  }
}

console.log("\n=== AI Engineering from Scratch — Environment Check (TS) ===\n");

const results = CHECKS.map(runCheck);
const passed = results.filter(Boolean).length;
const total = CHECKS.length;

console.log(`\nResult: ${passed}/${total} checks passed`);

if (passed === total) {
  console.log("\nYou're ready. Start with Phase 1.\n");
  process.exit(0);
} else {
  console.log("\nFix the failed checks above, then run this script again.\n");
  process.exit(1);
}
