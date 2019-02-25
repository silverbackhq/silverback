workflow "New workflow" {
  on = "push"
  resolves = ["clivern/gh-action-python@baedab7975be47bfcafebb87323b01469cd10e2b"]
}

action "clivern/gh-action-python@baedab7975be47bfcafebb87323b01469cd10e2b" {
  uses = "clivern/gh-action-python@baedab7975be47bfcafebb87323b01469cd10e2b"
  runs = "make"
  args = "ci"
}
