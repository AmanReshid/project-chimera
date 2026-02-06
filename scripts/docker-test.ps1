param(
    [switch]$NoCache,
    [string]$ImageName = "project-chimera",
    [string]$PythonVersion = "3.14-slim"
)

# Build args for the builder stage that runs tests during build
$buildArgs = @(
    '--target', 'builder',
    '--build-arg', 'RUN_TESTS=true',
    '--build-arg', "PYTHON_VERSION=$PythonVersion",
    '-t', "$ImageName:test",
    '.'
)

if ($NoCache) { $buildArgs = @('--no-cache') + $buildArgs }

Write-Host "Running: docker build $($buildArgs -join ' ')"

& docker @buildArgs
if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build (tests) failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Docker builder tests completed successfully. Image: $ImageName:test"
