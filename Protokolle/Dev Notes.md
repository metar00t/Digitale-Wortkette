# Developer Notes
## Game Session
### Timeout System (Player)
- Timeout Player if disconnected / Idle?
  - After how many Seconds (or Minutes)? 
### Turn Order Logic (done)
```python
list = ["String1","String2","String3"]
list.append(list.pop(list.index(list[0])))
print(list) # Prints ["String2","String3","String1"]
```
### Player Identification / Correlation
- linking the IP Address to Player
  - Ask the Bossman about Possibility & potential Security Issues / Concerns
  - Reason: Easier to identify a disconnected Player with their IP (and their Token)

### Backend -> Frontend
- Testing current Game Logic Endpoints
  - Currently the Logic works when testing with Postman
  - Need to test if Frontend properly receives the Payload "As-Is"