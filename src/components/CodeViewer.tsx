import { useState } from "react";

const scriptSections = [
  {
    name: "Header & Parameters",
    lines: `# setup.ps1
# ERP v1.2.0 LTS — Windows 10 x64 only
# Production-oriented, idempotent setup script.
# Run from the repository root:
#   powershell -ExecutionPolicy Bypass -File .\\setup.ps1

[CmdletBinding()]
param(
    [switch]$SkipBuild,
    [switch]$SkipMigrations,
    [switch]$SkipOptional
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"`,
  },
  {
    name: "Logging Functions",
    lines: `function Write-Log {
    param(
        [Parameter(Mandatory)][string]$Message,
        [ValidateSet("INFO","WARN","ERROR")][string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] [$Level] $Message"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

function Fail {
    param([Parameter(Mandatory)][string]$Message)
    Write-Log -Message $Message -Level "ERROR"
    throw $Message
}`,
  },
  {
    name: "Step Execution",
    lines: `function Invoke-Step {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][scriptblock]$Action
    )
    Write-Log "START: $Name"
    try {
        & $Action
        Write-Log "PASS: $Name"
    }
    catch {
        Write-Log "FAIL: $Name :: $($_.Exception.Message)" -Level "ERROR"
        throw
    }
}

function Invoke-Native {
    param(
        [Parameter(Mandatory)][string]$FilePath,
        [Parameter()][string[]]$Arguments = @(),
        [Parameter(Mandatory)][string]$FailureMessage
    )
    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        Fail "$FailureMessage ExitCode=$LASTEXITCODE"
    }
}`,
  },
  {
    name: "Validation Steps",
    lines: `function Test-Windows10 {
    $productName = (Get-ItemProperty \\
        "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" \\
        -Name ProductName -ErrorAction Stop).ProductName
    if ($productName -notmatch "Windows 10") {
        Fail "Unsupported OS: $productName"
    }
}

function Test-Architecture {
    if ($env:PROCESSOR_ARCHITECTURE -ne "AMD64") {
        Fail "Unsupported architecture: $env:PROCESSOR_ARCHITECTURE"
    }
}

function Test-AdministrativeAccess {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    if (-not $principal.IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Fail "Administrator privileges required."
    }
}`,
  },
  {
    name: "Node.js Installation",
    lines: `function Install-NodeProject {
    param([Parameter(Mandatory)][System.IO.FileInfo]$PackageFile)
    $projectDir = $PackageFile.Directory.FullName
    Push-Location $projectDir
    try {
        $lockNpm = Test-Path (Join-Path $projectDir "package-lock.json")
        $lockPnpm = Test-Path (Join-Path $projectDir "pnpm-lock.yaml")
        $lockYarn = Test-Path (Join-Path $projectDir "yarn.lock")

        if ($lockNpm) {
            Invoke-Native -FilePath "npm.cmd" \\
                -Arguments @("ci","--include=optional") \\
                -FailureMessage "npm ci failed."
        }
        elseif ($lockPnpm) {
            Invoke-Native -FilePath "pnpm.cmd" \\
                -Arguments @("install","--frozen-lockfile") \\
                -FailureMessage "pnpm install failed."
        }
        elseif ($lockYarn) {
            Invoke-Native -FilePath "yarn.cmd" \\
                -Arguments @("install","--frozen-lockfile") \\
                -FailureMessage "yarn install failed."
        }
    }
    finally { Pop-Location }
}`,
  },
  {
    name: "Python Environment",
    lines: `function Initialize-PythonProject {
    param([Parameter(Mandatory)][System.IO.FileInfo]$RequirementsFile)
    $projectDir = $RequirementsFile.Directory.FullName
    $venvDir = Join-Path $projectDir ".venv"

    Push-Location $projectDir
    try {
        if (-not (Test-Path $venvDir)) {
            Invoke-Native -FilePath "py.exe" \\
                -Arguments @("-3.12","-m","venv",".venv") \\
                -FailureMessage "venv creation failed."
        }
        $pythonExe = Join-Path $venvDir "Scripts\\python.exe"
        Invoke-Native -FilePath $pythonExe \\
            -Arguments @("-m","pip","install",
                "--upgrade","pip","setuptools","wheel") \\
            -FailureMessage "pip bootstrap failed."
        Invoke-Native -FilePath $pythonExe \\
            -Arguments @("-m","pip","install","-r",
                $RequirementsFile.Name) \\
            -FailureMessage "pip install failed."
    }
    finally { Pop-Location }
}`,
  },
  {
    name: "Main Execution",
    lines: `$RepoRoot = Get-RepoRoot
Initialize-State

Invoke-Step "Validate Windows 10" { Test-Windows10 }
Invoke-Step "Validate Windows 10 x64" { Test-Architecture }
Invoke-Step "Validate administrator access" { Test-AdministrativeAccess }
Invoke-Step "Validate PowerShell" { ... }
Invoke-Step "Validate repository" { ... }
Invoke-Step "Validate required runtime tooling" { ... }
Invoke-Step "Prepare application data directories" { ... }
Invoke-Step "Install Node dependencies" { ... }
Invoke-Step "Initialize Python environments" { ... }

if (-not $SkipMigrations) {
    Invoke-Step "Run database migrations" { ... }
}
if (-not $SkipBuild) {
    Invoke-Step "Build Node applications" { ... }
}

Invoke-Step "Validate generated artifacts" { ... }
Invoke-Step "Write setup state" { Save-State -Completed $true }`,
  },
];

export default function CodeViewer() {
  const [activeSection, setActiveSection] = useState(0);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-100 mb-3">
          Source Code
        </h2>
        <p className="text-gray-400 max-w-xl mx-auto">
          Key sections of the setup.ps1 script. Click a section to view its implementation.
        </p>
      </div>

      <div className="rounded-xl border border-gray-800 bg-gray-900/50 overflow-hidden">
        {/* Section tabs */}
        <div className="flex overflow-x-auto border-b border-gray-800 bg-gray-950/50">
          {scriptSections.map((section, index) => (
            <button
              key={section.name}
              onClick={() => setActiveSection(index)}
              className={`px-4 py-3 text-xs whitespace-nowrap transition-colors border-b-2 ${
                activeSection === index
                  ? "border-emerald-400 text-emerald-400 bg-gray-900/50"
                  : "border-transparent text-gray-500 hover:text-gray-300"
              }`}
            >
              {section.name}
            </button>
          ))}
        </div>

        {/* Code display */}
        <div className="p-6 overflow-x-auto">
          <pre className="text-sm leading-relaxed">
            <code className="text-gray-300">
              {scriptSections[activeSection].lines.split("\n").map((line, i) => (
                <div key={i} className="flex">
                  <span className="inline-block w-8 text-right mr-4 text-gray-600 select-none text-xs leading-relaxed">
                    {i + 1}
                  </span>
                  <span className="flex-1">
                    {highlightLine(line)}
                  </span>
                </div>
              ))}
            </code>
          </pre>
        </div>
      </div>
    </div>
  );
}

function highlightLine(line: string): JSX.Element {
  // Simple syntax highlighting
  if (line.trim().startsWith("#")) {
    return <span className="text-gray-500 italic">{line}</span>;
  }
  
  // Keywords
  const keywords = /\b(function|param|if|else|elseif|try|catch|finally|throw|return|foreach|while|for|switch)\b/g;
  const strings = /("[^"]*"|'[^']*')/g;
  const variables = /(\$[\w]+)/g;
  const comments = /(#.*)$/;
  
  let result = line;
  
  // Check for inline comment
  const commentMatch = result.match(comments);
  if (commentMatch && !result.trim().startsWith("#")) {
    const beforeComment = result.substring(0, commentMatch.index);
    const comment = commentMatch[0];
    return (
      <span>
        {highlightSyntax(beforeComment)}
        <span className="text-gray-500 italic">{comment}</span>
      </span>
    );
  }
  
  return <span>{highlightSyntax(result)}</span>;
}

function highlightSyntax(text: string): JSX.Element {
  const parts: JSX.Element[] = [];
  let remaining = text;
  let key = 0;

  // Process strings first
  const stringRegex = /("[^"]*"|'[^']*')/g;
  let lastIndex = 0;
  let match;

  while ((match = stringRegex.exec(remaining)) !== null) {
    // Text before string
    if (match.index > lastIndex) {
      const before = remaining.substring(lastIndex, match.index);
      parts.push(<span key={key++}>{highlightKeywords(before)}</span>);
    }
    // The string itself
    parts.push(<span key={key++} className="text-amber-300">{match[0]}</span>);
    lastIndex = match.index + match[0].length;
  }

  // Remaining text after last string
  if (lastIndex < remaining.length) {
    const after = remaining.substring(lastIndex);
    parts.push(<span key={key++}>{highlightKeywords(after)}</span>);
  }

  if (parts.length === 0) {
    return <span>{highlightKeywords(text)}</span>;
  }

  return <>{parts}</>;
}

function highlightKeywords(text: string): JSX.Element {
  const keywords = ["function", "param", "if", "else", "elseif", "try", "catch", "finally", "throw", "return", "foreach", "while", "for", "switch", "ValidateSet", "CmdletBinding", "Parameter", "Mandatory"];
  const builtins = ["Set-StrictMode", "Write-Host", "Write-Log", "Get-Command", "Get-ItemProperty", "Get-ChildItem", "Test-Path", "New-Item", "Join-Path", "Resolve-Path", "Add-Content", "Set-Content", "ConvertTo-Json", "ConvertFrom-Json", "Get-Content", "Get-Date", "Get-Item", "Where-Object", "Select-Object", "Push-Location", "Pop-Location", "Invoke-Native", "Invoke-Step", "Require-Command", "Initialize-State", "Save-State", "Fail"];

  let result = text;
  
  // Highlight variables
  result = result.replace(/(\$[\w:]+)/g, '<var>$1</var>');
  
  // Highlight keywords
  keywords.forEach(kw => {
    const regex = new RegExp(`\\b(${kw})\\b`, "g");
    result = result.replace(regex, `<kw>${kw}</kw>`);
  });

  // Highlight builtins
  builtins.forEach(bi => {
    const regex = new RegExp(`\\b(${bi})\\b`, "g");
    result = result.replace(regex, `<bi>${bi}</bi>`);
  });

  // Convert markers to spans
  const parts = result.split(/(<var>.*?<\/var>|<kw>.*?<\/kw>|<bi>.*?<\/bi>)/g);
  
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith("<var>")) {
          return <span key={i} className="text-sky-400">{part.replace(/<\/?var>/g, "")}</span>;
        }
        if (part.startsWith("<kw>")) {
          return <span key={i} className="text-purple-400">{part.replace(/<\/?kw>/g, "")}</span>;
        }
        if (part.startsWith("<bi>")) {
          return <span key={i} className="text-cyan-400">{part.replace(/<\/?bi>/g, "")}</span>;
        }
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}
