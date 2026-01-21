"""
Claude Code CLI Client wrapper for AI Skill Factory.
Uses subprocess to call Claude Code CLI for content generation.
"""

import subprocess
import sys
import shutil
from typing import Optional


def _find_claude_executable() -> str:
    """Find the claude executable, handling Windows .cmd extension."""
    # Try to find claude in PATH
    claude_path = shutil.which("claude")
    if claude_path:
        return claude_path

    # On Windows, try claude.cmd explicitly
    if sys.platform == "win32":
        claude_cmd = shutil.which("claude.cmd")
        if claude_cmd:
            return claude_cmd

    # Fallback to just "claude" and let subprocess handle it
    return "claude"


class ClaudeCodeClient:
    """Wrapper for Claude Code CLI with subprocess execution."""

    def __init__(self, model: str = "sonnet") -> None:
        """Initialize the Claude Code CLI client.

        Args:
            model: Model to use (sonnet, opus, haiku). Defaults to sonnet.
        """
        self.model = model
        self.max_retries = 2
        self.timeout = 300  # 5 minutes timeout
        self.claude_exe = _find_claude_executable()

        self._verify_claude_cli()
        print("[Init] Claude Code CLI client initialized")

    def _verify_claude_cli(self) -> None:
        """Verify claude CLI is available and working."""
        try:
            result = subprocess.run(
                [self.claude_exe, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                encoding="utf-8",
                shell=(sys.platform == "win32"),
            )
            if result.returncode != 0:
                raise RuntimeError("Claude CLI not responding")
            version_info = result.stdout.strip() or result.stderr.strip()
            print(f"  Claude CLI: {version_info}")
        except FileNotFoundError:
            raise RuntimeError(
                "Claude CLI not found. Install with: npm install -g @anthropic-ai/claude-code"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Claude CLI verification timed out")

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate content using Claude Code CLI.

        Args:
            prompt: The user prompt to send
            system: Optional system prompt
            max_tokens: Maximum tokens (note: CLI doesn't support this directly)
            temperature: Temperature (note: CLI doesn't support this directly)

        Returns:
            Generated text response

        Note:
            max_tokens and temperature are accepted for API compatibility
            but are not directly controllable via CLI.
        """
        cmd = [
            self.claude_exe,
            "-p",  # Print mode (non-interactive)
            "--model", self.model,
            "--output-format", "text",
        ]

        # Add system prompt if provided
        if system:
            cmd.extend(["--system-prompt", system])

        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                print(f"  [AI] Calling Claude CLI (attempt {attempt + 1})...", flush=True)

                result = subprocess.run(
                    cmd,
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    encoding="utf-8",
                    shell=(sys.platform == "win32"),
                )

                if result.returncode != 0:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                    print(f"    - Error (code {result.returncode}): {error_msg}")
                    last_error = RuntimeError(f"Claude CLI failed: {error_msg}")
                    if attempt < self.max_retries:
                        continue
                    raise last_error

                response = result.stdout.strip()
                if not response:
                    print("    - Empty response, retrying...")
                    last_error = RuntimeError("Empty response from Claude CLI")
                    if attempt < self.max_retries:
                        continue
                    raise last_error

                print("  [AI] Success")
                return response

            except subprocess.TimeoutExpired:
                print(f"    - Timeout after {self.timeout}s, retrying...")
                last_error = RuntimeError(f"Claude CLI timed out after {self.timeout}s")
                if attempt >= self.max_retries:
                    raise last_error

            except Exception as e:
                if isinstance(e, RuntimeError):
                    raise
                print(f"    - Unexpected error: {e}")
                last_error = e
                if attempt >= self.max_retries:
                    raise RuntimeError(f"Claude CLI failed: {e}") from e

        raise RuntimeError(f"All retry attempts failed. Last error: {last_error}")
