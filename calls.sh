curl -s -X POST localhost:5000/api/users.admin.invite -F 'email=one@local'
sleep 1
curl -s -X POST localhost:5000/api/users.admin.invite -F 'email=two@local'
sleep 1
curl -s -X POST localhost:5000/api/users.admin.invite -F 'email=three@local'
sleep 1
curl -s -X POST localhost:5000/meta/invite.accept -F 'email=two@local'
sleep 1
curl -s -X POST localhost:5000/meta/invite.accept.all
sleep 1

next_cursor=''

while true
do
    r="$(curl -F 'limit=1' -F "next_cursor=$next_cursor" -s -X POST localhost:5000/api/users.list | jq -r '.response_metadata.next_cursor as $n | .members[] | [.id, .profile.email, $n] | @csv' | tr -d '"')"
    echo "$r"
    sleep 1
    next_cursor="$(cut -f 3 -d ',' <<< "$r")"
    echo $next_cursor
    [ -z "$next_cursor" ] && break
done
