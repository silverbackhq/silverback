workflow "New workflow" {
  on = "push"
  resolves = ["Testing"]
}

action "Testing" {
  uses = "https://github.com/Clivern/gh-action-python"
  args = "make"
  runs = "ci"
}
