# kiro-cli-jenkins-build-triage

AI-powered build failure triage and auto-fix using [Kiro CLI](https://kiro.dev/cli/) headless mode in a Jenkins pipeline. When a build fails, Kiro reads the test output and git diff, identifies the root cause, writes the fix, commits it to a new branch, pushes it, and opens a pull request — all automatically.

## How It Works

```
Build fails → Kiro reads test log + diff → Identifies root cause → Writes fix → Commits → Pushes branch → Opens PR
```

The sample app is a minimal [Strands](https://strandsagents.com/) weather agent with a single tool and two unit tests. The app is intentionally simple — the demo is the Jenkinsfile.

## What Kiro Does on Failure

1. Reads `test-output.log` and the git diff from the last commit
2. Identifies the root cause and maps it to the code change
3. Edits the source files directly using the `write` tool
4. The pipeline then commits, pushes a fix branch, and opens a PR via the GitHub API

Typical triage: **3-4 seconds, ~$0.03 per run**.

## Project Structure

```
agent.py           — Strands weather agent (11 lines)
tools.py           — Weather lookup tool using wttr.in (no API key needed)
test_tools.py      — Unit tests
Jenkinsfile        — Pipeline with Kiro headless triage + auto-fix + PR creation
Dockerfile         — Container image (for optional ECR deployment)
requirements.txt   — Python dependencies
```

## Prerequisites

- **Jenkins** with Pipeline plugin
- **Python 3** available on the Jenkins agent
- **Kiro CLI** installed on the Jenkins agent
- **GitHub personal access token** (classic, with `repo` scope)

## Setup

### 1. Jenkins (Docker)

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

Get the admin password:
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open http://localhost:8080, complete setup, install suggested plugins.

### 2. Install Python in the Jenkins container

```bash
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y python3 python3-pip python3-venv"
```

### 3. Install Kiro CLI in the Jenkins container

```bash
docker exec jenkins bash -c "curl -fsSL https://cli.kiro.dev/install | bash"
```

### 4. Add Jenkins credentials

Go to **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**:

| ID | Kind | Value |
|---|---|---|
| `kiro-api-key` | Secret text | Your Kiro API key (from https://app.kiro.dev) |
| `github-token` | Secret text | GitHub personal access token with `repo` scope |

### 5. Create the pipeline job

1. **New Item → Pipeline** → name it (e.g., `kiro-build-triage`)
2. **Pipeline → Definition**: Pipeline script from SCM
3. **SCM**: Git → Repository URL: your fork of this repo
4. **Branches to build**: `*/main`
5. **Script Path**: `Jenkinsfile`
6. **Save**

### 6. Run a green build first

Make sure `tools.py` has `temp_F` (not `temp_X`). Click **Build Now**. It should pass.

## Demo: Trigger the Auto-Fix

Introduce a bug:
```bash
sed -i 's/temp_F/temp_X/' tools.py
git add tools.py && git commit -m "introduce bug"
git push
```

Click **Build Now**. The pipeline will:
1. Fail at the Test stage (`KeyError: 'temp_X'`)
2. Kiro reads the test log and diff
3. Kiro identifies the root cause and writes the fix
4. Commits as "Kiro Bot" on a `fix/kiro-auto-fix-N` branch
5. Pushes the branch and opens a PR

Check your GitHub repo for the new PR.

## Key Jenkinsfile Details

- `set -o pipefail` ensures pytest failures propagate through `tee`
- `--no-interactive` runs Kiro without prompts
- `--trust-tools=read,grep,write` lets Kiro read files and write fixes
- `GIT_ASKPASS` handles GitHub auth without Jenkins credential masking issues
- PR creation uses `curl` to the GitHub REST API (standard CI/CD pattern)

## Customization

- **Change the prompt** in the Jenkinsfile `post { failure {} }` block to adjust what Kiro analyzes
- **Add more trusted tools** (e.g., `--trust-tools=read,grep,write,shell`) to let Kiro run tests after fixing — note: `shell` is blocked in `--no-interactive` mode by default
- **Swap the sample app** for any project with tests — the Kiro triage stage is app-agnostic

## Cost

Kiro CLI charges per use. Typical build triage costs ~$0.03-0.16 depending on the complexity of the failure and number of files read.

## License

MIT
