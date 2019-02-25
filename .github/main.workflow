workflow "Testing" {
  on = "push"
  resolves = ["https://github.com/Clivern/gh-action-python"]
}

action "https://github.com/Clivern/gh-action-python" {
  uses = "https://github.com/Clivern/gh-action-python"
  runs = "make ci"
}
