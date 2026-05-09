# OPETreeWB – Test Specification

This document lists all test files and describes
what each test validates.

All tests are executed **inside FreeCAD**.

----

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

----

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

----

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

----

### T0008.py

**Purpose:**  
Validate rollback of staged overlay changes using work/discard.

**What is validated:**

*   Overlay data is removed successfully
*   No changes are committed to live data
*   Session remains usable or reset depending on API behavior
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that work/discard:
- removes all staged changes in overlay
- prevents any persistence to live tables
- resets session state for clean workflow continuation

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

1. Call work/discard API  
2. Remove staged overlay changes  
3. Validate working state remains accessible  
4. Confirm no staged data remains  

#### Expected Results

✅ Overlay table (`<domain>_data_overlay`) is cleared  
✅ No changes appear in live table  
✅ Session can proceed without residual state  
✅ No exceptions are raised  

#### Backend Validation

Verify:

- Overlay table is empty for the active session  
- Live table (`<domain>_data`) remains unchanged  
- No new history entries are created  

#### Success Criteria

Test passes if:

- Overlay is cleared successfully  
- No unintended persistence occurs  
- System remains stable for next operations  

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| overlay still contains data | discard failed |
| data appears in live table | incorrect commit behavior |
| HTTP 409 | session not active |
| HTTP 400 | incorrect API call |
| connection refused | API server not running |

#### Notes

- This is the **rollback branch of workflow**  
- Opposite of T0007 (commit)
- Ensures safe undo of staged changes

----

### T0009.py

**Purpose:**  
Validate attribute API operations (CREATE / UPDATE / DELETE).

**What is validated:**

*   Attribute creation via work/push
*   Attribute update via work/push
*   Attribute deletion via work/push
*   No exceptions during operations

**Layer:**  
Integration

----

### T0010.py

**Purpose:**  
Validate node creation using schema-defined attribute IDs and sparse storage model.

**What is validated:**

*   Node is created with only mandatory base attributes (Name, Type, Owner)
*   Attribute IDs match schema-defined values (1, 2, 3)
*   Identity rule is satisfied (Name.data_id == node_id)
*   Attribute values are correctly assigned (Type, Owner)
*   No unexpected attributes are stored

**Layer:**  
Integration

#### Objective

Verify that node creation:
- uses schema-defined attribute IDs
- stores only required attributes (sparse model)
- correctly assigns values for Type and Owner
- enforces identity rule

#### Scope

Validates integration of:

- api/node_api.py
- api/query_api.py
- hierarchy schema (base_attributes)

#### Preconditions

- ✅ T0004 executed (active session exists)  
- ✅ OPE_DB_API server is running  
- ✅ PostgreSQL database is available  

#### Input Configuration

| Parameter | Value |
|----------|------|
| parent_node_id | 1000 |
| type | STRA |
| name | default ("") |

#### Execution Summary

The test performs:

1. Create a node using NodeAPI  
2. Query node attributes using search API  
3. Validate total attribute count (must be 3)  
4. Validate each attribute:
   - Name → identity rule
   - Type → correct value
   - Owner → correct parent mapping  

#### Expected Results

✅ Exactly 3 attributes are stored (Name, Type, Owner)  
✅ Name attribute uses data_id == node_id  
✅ Type attribute value equals "STRA"  
✅ Owner attribute value equals 1000  
✅ No additional attributes are stored

#### Backend Validation

Verify:

- 3 rows exist in `<domain>_data_overlay`  
- attribute_id values:
  - 1 → Name  
  - 2 → Type  
  - 3 → Owner  
- data_id of Name row == node_id  
- No other attribute rows exist  

#### Success Criteria

Test passes if:

- Node has exactly 3 attributes  
- All attribute IDs match schema  
- Identity rule is satisfied  
- No runtime errors occur  

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| attribute count ≠ 3 | schema logic incorrect |
| identity rule fails | wrong data_id assignment |
| Type mismatch | incorrect value logic |
| Owner mismatch | parent mapping error |
| unexpected attribute_id | schema mapping bug |
| HTTP error | session/API issue |

#### Notes

- This test confirms **sparse storage model**  
- Default schema attributes are NOT stored  
- Schema acts as fallback during rendering  
- This is the baseline for all node-based workflows  

----

### T0011.py

**Purpose:**  
Validate node deletion and attribute cleanup.

**What is validated:**

*   Node deletion removes all associated attribute rows
*   Node is no longer retrievable via API
*   No residual data exists after deletion
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that node deletion:
- removes all attributes of a node
- ensures no orphan data remains
- reflects correctly in query results

#### Scope

Validates integration of:

- api/node_api.py
- api/query_api.py

#### Preconditions

- ✅ T0004 executed (active session exists)  
- ✅ OPE_DB_API server is running  
- ✅ PostgreSQL database is available  

#### Execution Summary

The test performs:

1. Create a node  
2. Delete the node using NodeAPI  
3. Query for node  
4. Verify node no longer exists  

#### Expected Results

✅ No records exist for node_id after deletion  
✅ All attribute rows are removed  
✅ No exceptions are raised  

#### Backend Validation

Verify:

- No rows exist in `<domain>_data_overlay` for node_id  
- After commit → no rows in `<domain>_data` either  
- No orphan rows present  

#### Success Criteria

Test passes if:

- Node is fully removed  
- Query returns empty result  
- No runtime errors occur  

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| node still exists | delete incomplete |
| partial attributes remain | cascade failure |
| HTTP error | session/API issue |
| stale overlay data | discard/save mismatch |

#### Notes

- This test validates **delete cascade behavior**  
- Ensures **data integrity after removal**  
- Critical for maintaining clean graph structure  

----

### T0012.py

**Purpose:**  
Validate local session creation using the same session_id as API session.

**What is validated:**

*   Local session is created using OPE_DB_API CRUD layer
*   Same session_id is reused from API session (no duplication)
*   Session is marked active in local DB
*   Context consistency between API and local layer
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that local session:
- uses the same session_id generated by API (T0004)
- is correctly inserted into local DB
- is marked as active
- ensures consistent session behavior across API and local layers

#### Scope

Validates integration of:

- local/session_local.py
- local/client.py
- local/bootstrap.py
- OPE_DB_API.crud.session.start

#### Preconditions

- ✅ T0004 executed (API session must exist)  
- ✅ OPE_DB_CONTEXT is initialized  
- ✅ OPE_DB_API server is running  
- ✅ Local PostgreSQL is configured and reachable

#### Input Configuration

| Parameter | Value |
|----------|------|
| session_id | OPE_DB_CONTEXT.session_id |
| username | Shivang |
| hostname | PCS |
| domain | SKET |

#### Execution Summary

The test performs:

1. Execute T0004 to create API session  
2. Reuse same `session_id` from context  
3. Call `SessionLocal.start()`  
4. Validate returned session object  
5. Verify session is active  

#### Expected Results

✅ Session row is created in local DB  
✅ `session.active == True`  
✅ `session.session_id == OPE_DB_CONTEXT.session_id`  
✅ No duplicate session IDs  
✅ No exceptions occur  

#### Backend Validation

Verify in local DB:

- A row exists in `session_metadata`  
- `session_id` matches API session  
- `active = True`  
- `username = Shivang`  
- `hostname = PCS`  
- `domain = SKET`  
- `ended_at IS NULL`  

#### Success Criteria

Test passes if:

- Local session is created successfully  
- Session ID matches API session ID  
- Session is active  
- No runtime errors occur  

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| session not created | CRUD integration issue |
| inactive session | incorrect insert logic |
| session_id mismatch | improper reuse of API session |
| duplicate entry error | session already exists |
| DB connection error | config/bootstrap issue |

#### Notes

- This test validates **hybrid session consistency (API + Local)**  
- Local session MUST reuse API-generated session_id  
- Ensures both layers operate under a unified session model  
- This is critical for overlay synchronization between API and local DB

----

### T0013.py

**Purpose:**
Validate local session closure using the same session_id as API session.

**What is validated:**

*   Local session is correctly closed using CRUD layer
*   Session is marked inactive in local DB
*   Same session_id (from API) is used for closure
*   Session lifecycle consistency between API and local layer
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that local session close:
- updates session state to inactive
- sets ended_at timestamp
- maintains consistency with API session lifecycle

#### Scope

Validates integration of:

- local/session_local.py
- local/client.py
- local/bootstrap.py
- OPE_DB_API.crud.session.close

#### Preconditions

- ✅ T0004 executed (API session exists)  
- ✅ T0012 executed (local session created)  
- ✅ OPE_DB_CONTEXT is initialized  
- ✅ Local PostgreSQL is configured and reachable

#### Input Configuration

| Parameter | Value |
|----------|------|
| session_id | OPE_DB_CONTEXT.session_id |

#### Execution Summary

The test performs:

1. Execute T0004 (API session start)  
2. Execute T0012 (local session start)  
3. Call `SessionLocal.close()` using same session_id  
4. Validate session state

#### Expected Results

✅ Session is marked inactive in local DB  
✅ `session.active == False`  
✅ `ended_at IS NOT NULL`  
✅ Session_id matches API session  
✅ No exceptions occur

#### Backend Validation

Verify in local DB:

- Row exists in `session_metadata`  
- `active = False`  
- `ended_at` is populated  
- `session_id` matches API session

#### Success Criteria

Test passes if:

- Session is successfully closed  
- Session state is inactive  
- No runtime errors occur

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| session still active | close logic failed |
| ended_at not set | DB update failure |
| invalid session_id | mismatch with API |
| DB connection error | config/bootstrap issue |

#### Notes

- This test completes **local session lifecycle**  
- Works together with:
  - T0004 (API session start)
  - T0012 (local session start)  
- Ensures a **single unified session model** across API and local layers  
- Critical for maintaining consistent overlay and transaction behavior

----

### T0014.py

**Purpose:**  
Validate local session closure using the same session_id as API session.

**What is validated:**

*   Local session is correctly closed using CRUD layer
*   Session is marked inactive in local DB
*   Same session_id (from API) is used for closure
*   Session lifecycle consistency between API and local layer
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that local session close:
- updates session state to inactive
- sets ended_at timestamp
- maintains consistency with API session lifecycle

#### Scope

Validates integration of:

- local/session_local.py
- local/client.py
- local/bootstrap.py
- OPE_DB_API.crud.session.close

#### Preconditions

- ✅ T0004 executed (API session exists)  
- ✅ T0012 executed (local session created)  
- ✅ OPE_DB_CONTEXT is initialized  
- ✅ Local PostgreSQL is configured and reachable

#### Input Configuration

| Parameter | Value |
|----------|------|
| session_id | OPE_DB_CONTEXT.session_id |

#### Execution Summary

The test performs:

1. Execute T0004 (API session start)  
2. Execute T0012 (local session start)  
3. Call `SessionLocal.close()` using same session_id  
4. Validate session state

#### Expected Results

✅ Session is marked inactive in local DB  
✅ `session.active == False`  
✅ `ended_at IS NOT NULL`  
✅ Session_id matches API session  
✅ No exceptions occur

#### Backend Validation

Verify in local DB:

- Row exists in `session_metadata`  
- `active = False`  
- `ended_at` is populated  
- `session_id` matches API session

#### Success Criteria

Test passes if:

- Session is successfully closed  
- Session state is inactive  
- No runtime errors occur

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| session still active | close logic failed |
| ended_at not set | DB update failure |
| invalid session_id | mismatch with API |
| DB connection error | config/bootstrap issue |
#### Notes

- This test completes **local session lifecycle**
- Works together with:
  - T0004 (API session start)
  - T0012 (local session start)
- Ensures a **single unified session model** across API and local layers
- Critical for maintaining consistent overlay and transaction behavior

----

### T0015.py

**Purpose:**  
Validate local commit operation (overlay → live).

**What is validated:**

*   Overlay changes are applied to live table
*   History entries are created
*   Overlay is cleared after commit
*   Session is closed
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that local commit:
- moves overlay data to live table
- creates history entries
- clears overlay table
- closes session

#### Scope

Validates integration of:

- local/attribute_local.py
- local/query_local.py
- local/client.py
- OPE_DB_API.crud.commit.commit

#### Preconditions

- ✅ T0004 executed (API session)
- ✅ T0012 executed (local session)
- ✅ T0014 executed (overlay data available)
- ✅ Local PostgreSQL available

#### Execution Summary

The test performs:

1. Execute overlay push (T0015)  
2. Call `commit_session()`  
3. Validate overlay is cleared  
4. Validate live table updated

#### Expected Results

✅ Data moved from overlay → live table  
✅ Overlay table is empty  
✅ Session is closed  
✅ No exceptions occur

#### Backend Validation

Verify:

- No rows remain in `<domain>_data_overlay`  
- Rows exist in `<domain>_data`  
- History entries created

#### Success Criteria

Test passes if:

- Overlay is cleared  
- Live table contains committed rows  
- No runtime errors occur

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| overlay not cleared | commit logic failed |
| live data missing | insert failed |
| exception thrown | invalid overlay state |
| session still active | close_session not executed |

#### Notes

- Mirrors API commit behavior (T0007)  
- Uses same backend logic (commit_session)  
- Ensures local DB behaves exactly like server  
- Critical for local-first architecture

----

### T0016.py

**Purpose:**  
Validate local abort operation (overlay discard).

**What is validated:**

*   Overlay data is cleared after abort
*   Live data remains unchanged
*   Session is closed
*   No exceptions occur during execution

**Layer:**  
Integration

#### Objective

Verify that local abort:
- removes all overlay data for the session
- does not modify live table
- closes session properly

#### Scope

Validates integration of:

- local/attribute_local.py
- local/query_local.py
- local/client.py
- OPE_DB_API.crud.session.abort

#### Preconditions

- ✅ T0004 executed (API session exists)
- ✅ T0012 executed (local session exists)
- ✅ T0014 executed (overlay contains data)
- ✅ Local PostgreSQL available

#### Execution Summary

The test performs:

1. Push attribute data into overlay (T0015)  
2. Call `abort_session()`  
3. Validate overlay is cleared  
4. Validate live table remains unchanged  

#### Expected Results

✅ Overlay table is cleared  
✅ Live table is unaffected  
✅ Session is closed  
✅ No exceptions occur  

#### Backend Validation

Verify:

- No rows exist in `<domain>_data_overlay`  
- No new entries in `<domain>_data`  
- Session is closed (`active = False`)

#### Success Criteria

Test passes if:

- Overlay is cleared  
- Live data untouched  
- No runtime errors occur

#### Failure Scenarios

| Failure | Possible Cause |
|--------|---------------|
| overlay still contains data | abort logic failed |
| live data changed | incorrect logic in abort |
| session still active | close_session not triggered |
| DB error | config/bootstrap issue |

#### Notes

- Mirrors API discard behavior (T0008)  
- Ensures local rollback is correct  
- Guarantees safe undo of staged changes

----

