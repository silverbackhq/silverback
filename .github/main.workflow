workflow "Testing" {
  resolves = ["https://github.com/Clivern/gh-action-python"]
  on = "push"
}

action "https://github.com/Clivern/gh-action-python" {
  uses = "https://github.com/Clivern/gh-action-python"
  runs = "make"
  args = "ci"
}