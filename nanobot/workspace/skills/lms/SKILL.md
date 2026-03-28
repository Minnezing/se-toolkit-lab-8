---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the LMS (Learning Management System) via MCP tools. Use these tools to provide real-time information about the course.

## Available Tools

- `lms_health` - Check if the LMS backend is healthy and get item count
- `lms_labs` - Get list of available labs
- `lms_pass_rates` - Get pass rates for a specific lab
- `lms_learner` - Get learner information
- `lms_timeline` - Get submission timeline for a lab
- `lms_groups` - Get group performance data
- `lms_top_learners` - Get top learners for a lab
- `lms_completion_rate` - Get completion rate for a lab
- `lms_sync_pipeline` - Trigger data sync

## Strategy

### When the user asks about scores, pass rates, completion, groups, timeline, or top learners WITHOUT naming a lab:

1. First call `lms_labs` to get the list of available labs
2. If multiple labs exist, ask the user to choose one
3. Present lab options using the lab title as the label
4. Once the user selects a lab, call the appropriate tool with the lab parameter

### When the user asks "what can you do?":

Explain that you can:
- Check LMS backend health
- List available labs
- Show pass rates, completion rates, and submission timelines for specific labs
- Show group performance and top learners
- Access learner information

Be clear about your current tools and limits - you can only access data through the LMS MCP tools.

### Formatting

- Format percentages with the % symbol (e.g., "75%" not "0.75")
- Format counts as whole numbers
- Keep responses concise but informative
- When showing data, mention which lab it's from

## Examples

**User:** "Show me the scores"
**You:** Call `lms_labs` first, then ask "Which lab would you like to see scores for? Here are the available labs: [list]"

**User:** "What labs are available?"
**You:** Call `lms_labs` and list them with their titles

**User:** "Is the backend healthy?"
**You:** Call `lms_health` and report the status and item count
