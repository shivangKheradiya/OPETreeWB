# OPETreeWB – Test Specification

This document lists all test files and describes
what each test validates.

All tests are executed **inside FreeCAD**.

---

## How to Run Tests

Open FreeCAD → Python Console and execute:

```python
from opetreewb.tests.run_tests import run_all
run_all()
````

***

## Test List

### T0001.py

**Purpose:**  
Validate static domain configuration rules.

**What is validated:**

*   Domain keys `DESI` and `DICT` exist
*   `RootType` values are correct
*   No unexpected mutation of domain rules

**Layer:**  
Domain (pure logic, no FreeCAD UI)

***

### T0002.py

**Purpose:**  
Validate unified node label formatting.

**What is validated:**
- Type + Name formatting
- Fallback to Node ID
- Fallback to default type when missing

**Layer:**
Domain

### T0003.py
**Purpose:**  
Ensure domain rules are treated as invariant configuration.

**What is validated:**
- Domain rules are not meant to be mutated at runtime
- Violations are detectable during development

**Layer:**  
Domain

----

### T0004.py

**Purpose:**  
Validate API session initialization and runtime context synchronization.

**What is validated:**

*   API session is successfully created
*   Session ID is generated (Snowflake-based)
*   Runtime context is correctly configured
*   Context reflects active session state
*   No exceptions occur during initialization

**Layer:**  
Integration

#### Objective

Verify that API-based session start:
- establishes a valid session in the backend
- correctly initializes runtime context
- prepares system for workflow operations


#### Scope

Validates integration of:

- core/context.py
- core/config.py
- api/client.py
- api/session_api.py


#### Preconditions

- ✅ OPE_DB_API server is running  
- ✅ PostgreSQL database is available  
- ✅ Valid project configuration exists  


#### Input Configuration

| Parameter | Value |
|----------|------|
| base_url | http://127.0.0.1:8000 |
| code | XYZ |
| domain | SKET |
| username | Shivang |
| hostname | PCS |



#### Execution Summary

The test performs:

1. Configure API base URL  
2. Initialize runtime context  
3. Start a new session via API  
4. Validate returned session ID  
5. Validate runtime context state  


#### Expected Results

✅ Session ID is generated (Snowflake ID, globally unique)  
✅ `OPE_DB_CONTEXT.is_session_active == True`  
✅ `OPE_DB_CONTEXT.session_id` matches returned session ID  
✅ No exceptions are raised  


#### Backend Validation

Verify in DB:

- A new row exists in SessionMetadata table  
- `session_id` matches generated ID  
- `active = True`  
- `username = Shivang`  
- `hostname = PCS`  
- `domain = SKET`  
- `ended_at IS NULL`  


#### Success Criteria

Test passes if:

- All validations succeed  
- Context remains consistent  
- API responds without errors  


#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| session_id is None | ID generation failure |
| context not active | session_api did not update context |
| session mismatch | context sync issue |
| HTTP error (404/409) | wrong base_url / code / domain |
| connection refused | API server not running |


#### Notes

- This test validates **session initialization only**  
- It does **NOT validate overlay/workflow operations**  
- It is the **entry point for all T00X API tests**  

---

### T0005.py

**Purpose:**  
Validate API session closure and runtime context cleanup.

**What is validated:**

*   Active session is successfully closed
*   Backend session state is updated (inactive)
*   Runtime context is cleared correctly
*   No exceptions occur during execution

**Layer:**  
Integration


#### Objective

Verify that API-based session close:
- deactivates session in backend
- clears runtime session context
- prevents further session-based operations


#### Scope

Validates integration of:

- core/context.py
- api/client.py
- api/session_api.py


#### Preconditions

- ✅ T0004 must be executed first (active session exists)  
- ✅ OPE_DB_API server is running  
- ✅ PostgreSQL database is available  


#### Execution Summary

The test performs:

1. Validate active session exists  
2. Call API session close  
3. Verify runtime context state  
4. Ensure session is no longer active  


#### Expected Results

✅ Session is closed in backend  
✅ `OPE_DB_CONTEXT.is_session_active == False`  
✅ Context no longer holds session_id  
✅ No exceptions are raised  


#### Backend Validation

Verify in DB:

- SessionMetadata row exists  
- `active = False`  
- `ended_at IS NOT NULL`  


#### Success Criteria

Test passes if:

- Session is properly closed  
- Context reflects inactive state  
- No runtime errors occur  


#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| session still active | API close not called or failed |
| context not updated | context cleanup issue |
| RuntimeError | T0004 not executed first |
| HTTP error (404/409) | invalid session_id |


#### Notes

- This test depends on T0004  
- Validates **session lifecycle completion**  
- Prepares system for next workflow tests  

---

### T0006.py

**Purpose:**  
Validate attribute staging into session overlay using work/push.

**What is validated:**

*   Attribute changes are staged correctly using API
*   Operation follows CREATE semantics (operation_type = 1)
*   Staged data is visible in working (overlay) state
*   No commit is triggered
*   No exceptions occur during execution

**Layer:**  
Integration


#### Objective

Verify that work/push:
- stages attribute changes into overlay
- makes changes visible in working state (live ⊕ overlay)
- does not persist data to live table yet

#### Scope

Validates integration of:

- api/client.py
- api/attribute_api.py
- api/query_api.py

#### Preconditions

- ✅ T0004 must be executed first (active session exists)  
- ✅ OPE_DB_API server is running  
- ✅ PostgreSQL database is available  

#### Execution Summary

The test performs:

1. Generate a test node_id and attribute_id  
2. Push attribute using API (CREATE operation)  
3. Query working state using search API  
4. Verify staged data exists in response  

#### Expected Results

✅ Attribute row is staged in overlay  
✅ data_id is generated correctly  
✅ Staged data appears in working state  
✅ No exceptions are raised  
✅ Data is NOT committed to live table  

#### Backend Validation

Verify:

- Row exists in `<domain>_data_overlay`  
- operation_type = 1  
- session_id matches active session  
- No entry in `<domain>_data` yet  

#### Success Criteria

Test passes if:

- Overlay contains staged data  
- Query returns expected row  
- No runtime errors occur  


#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| data not found in working state | push failed or wrong filter |
| RuntimeError | invalid attribute_id |
| HTTP 409 | session not active |
| HTTP 400 | payload mismatch |
| connection refused | API server not running |


#### Notes

- This is the first **workflow-level test (overlay)**
- Validates **intent staging, not persistence**
- Foundation for commit/discard testing

----

### T0007.py

**Purpose:**  
Validate commit of staged overlay changes into live data.

**What is validated:**

*   Overlay data is applied to live table
*   History entries are created
*   Overlay is cleared automatically
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that work/save:
- commits staged changes atomically
- moves overlay data to live storage
- records changes in history table
- closes session at backend level

#### Scope

Validates integration of:

- api/client.py
- api/query_api.py

#### Preconditions

- ✅ T0004 executed (session active)  
- ✅ T0006 executed (data staged in overlay)  
- ✅ OPE_DB_API server is running  

#### Execution Summary

The test performs:

1. Call work/commit, API  
2. Commit staged overlay changes  
3. Validate successful API response  

#### Expected Results

✅ Overlay data is applied to `<domain>_data`  
✅ Entries created in `<domain>_data_history`  
✅ Overlay table is cleared  
✅ No exceptions are raised  

#### Backend Validation

Verify:

- Data exists in `<domain>_data`  
- Overlay table `<domain>_data_overlay` is empty for session  
- History table contains new entries  
- Session is closed or marked inactive  

#### Success Criteria

Test passes if:

- Commit succeeds  
- Data is persisted in live table  
- Overlay is cleared  
- No runtime errors occur  

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| data not in live table | commit failed |
| overlay not cleared | save logic incomplete |
| HTTP 409 | session not active |
| HTTP 400 | invalid payload |
| connection refused | API server not running |

#### Notes

- This is the **commit step in workflow**  
- Converts intent (overlay) → truth (live data)  
- Enables next session cycle  

---
