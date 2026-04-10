#!/bin/bash

# Test script for Notes API
# Prerequisites: API must be running on localhost:8000

API_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

echo "Testing Notes API endpoints..."
echo "API URL: $API_URL"
echo ""

# Test 1: Health check
echo "1. Testing health check..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/")
if [ "$response" == "200" ]; then
    echo -e "${GREEN}✓ Health check passed${RESET}"
else
    echo -e "${RED}✗ Health check failed (status: $response)${RESET}"
    exit 1
fi

# Test 2: Create a note
echo "2. Testing create note..."
create_response=$(curl -s -X POST "$API_URL/api/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Note",
    "content": "This is a test note",
    "tags": ["test", "sample"]
  }')

note_id=$(echo "$create_response" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
if [ ! -z "$note_id" ]; then
    echo -e "${GREEN}✓ Create note passed (ID: $note_id)${RESET}"
else
    echo -e "${RED}✗ Create note failed${RESET}"
    echo "Response: $create_response"
    exit 1
fi

# Test 3: Get the note
echo "3. Testing get note..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/api/notes/$note_id")
if [ "$response" == "200" ]; then
    echo -e "${GREEN}✓ Get note passed${RESET}"
else
    echo -e "${RED}✗ Get note failed (status: $response)${RESET}"
    exit 1
fi

# Test 4: List notes
echo "4. Testing list notes..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/api/notes")
if [ "$response" == "200" ]; then
    echo -e "${GREEN}✓ List notes passed${RESET}"
else
    echo -e "${RED}✗ List notes failed (status: $response)${RESET}"
    exit 1
fi

# Test 5: Update note
echo "5. Testing update note..."
response=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$API_URL/api/notes/$note_id" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Test Note"
  }')
if [ "$response" == "200" ]; then
    echo -e "${GREEN}✓ Update note passed${RESET}"
else
    echo -e "${RED}✗ Update note failed (status: $response)${RESET}"
    exit 1
fi

# Test 6: Delete note
echo "6. Testing delete note..."
response=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$API_URL/api/notes/$note_id")
if [ "$response" == "204" ]; then
    echo -e "${GREEN}✓ Delete note passed${RESET}"
else
    echo -e "${RED}✗ Delete note failed (status: $response)${RESET}"
    exit 1
fi

# Test 7: Verify deletion
echo "7. Testing note is deleted..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/api/notes/$note_id")
if [ "$response" == "404" ]; then
    echo -e "${GREEN}✓ Note deletion verified${RESET}"
else
    echo -e "${RED}✗ Note still exists (status: $response)${RESET}"
    exit 1
fi

echo ""
echo -e "${GREEN}All tests passed!${RESET}"
