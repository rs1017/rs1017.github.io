---

# Generated Skill Creator

A meta-skill that helps you create new Claude Code skills by analyzing requirements, generating appropriate skill structures, and producing ready-to-use SKILL.md files with supporting scripts.

## When to Use This Skill

Invoke this skill when the user:
- Asks to "create a new skill for [task]"
- Describes a repetitive workflow that could be automated
- Wants to extend Claude Code with custom functionality
- Needs a specialized tool for their development workflow
- Says "I need a skill that does [specific task]"

## How It Works

1. **Requirement Analysis**: Analyzes user's problem description and extracts key requirements
2. **Skill Design**: Determines optimal skill structure (tools needed, scripts, references)
3. **Template Generation**: Creates SKILL.md with proper frontmatter and instructions
4. **Script Generation**: Generates supporting Python/Bash scripts if needed
5. **Validation**: Ensures skill follows naming conventions and best practices

## Usage

```
User: I need a skill that analyzes my Git commit history and suggests improvements

Claude: I'll create a git-commit-analyzer skill for you...
[Generates complete skill package with SKILL.md and analysis script]
```

## Skill Structure

```
.claude/skills/generated-skill/
├── SKILL.md                 # Main skill definition
├── scripts/
│   └── skill_generator.py   # Skill generation logic
└── assets/
    └── template.md          # SKILL.md template
```

## Implementation

The skill uses these steps:

### 1. Parse User Requirements

Extract:
- Problem domain (git, files, API, etc.)
- Desired outcome
- Input/output formats
- Complexity level

### 2. Determine Skill Components

Decide if skill needs:
- Python/Bash scripts
- Reference documents
- Templates or assets
- External API calls

### 3. Generate SKILL.md

Create proper frontmatter:
```yaml
---
name: [lowercase-with-hyphens]
description: [What it does and when to use it]
---
```

### 4. Create Supporting Files

Generate any needed:
- `scripts/*.py` - Python automation
- `scripts/*.sh` - Bash commands
- `references/*.md` - Documentation
- `assets/*` - Templates, configs

### 5. Output Complete Package

Provide user with:
- Full SKILL.md content
- All supporting files
- Installation instructions
- Usage examples

## Best Practices

1. **Naming**: Always use lowercase-with-hyphens format
2. **Triggers**: Include clear "when to use" conditions in description
3. **Self-Contained**: Skills should work independently
4. **Documentation**: Include examples and error handling
5. **Validation**: Check for naming conflicts before creating

## Example Generated Skills

### Simple Skill (No Scripts)
```yaml
---
name: markdown-table-formatter
description: Formats markdown tables with proper alignment and spacing. Use when markdown tables are misaligned or need consistent formatting.
---
```

### Complex Skill (With Scripts)
```yaml
---
name: api-response-mocker
description: Generates mock API responses from OpenAPI specs. Use when developing frontend before backend is ready.
---
```

## Error Handling

- If skill name conflicts with existing skill, suggest alternatives
- If requirements are unclear, ask clarifying questions
- If external dependencies needed, warn user and provide installation steps

## Limitations

- Cannot modify existing skills (use edit tools instead)
- Cannot access external APIs during generation
- Generated scripts need user review before execution
- May need manual adjustment for complex workflows

## Related Skills

- `skill-creator` - Interactive skill creation wizard
- `command-generator` - Creates slash commands
- `hook-creator` - Creates Claude Code hooks