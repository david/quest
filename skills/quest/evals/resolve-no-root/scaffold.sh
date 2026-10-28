. "$(dirname "$0")/../_fixture/realm.sh"
drop_home_repo
provide_git
printf '# Notes\n\nScratch notes, not a realm.\n' >"$REALM/README.md"
