TEST_DATA=$(cat test/data_01.txt | base64)
echo $TEST_DATA

curl -X POST --data "$TEST_DATA" --header "Content-Type: application/json" http://localhost:5000/check