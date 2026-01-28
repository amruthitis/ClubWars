
#  Smart Logistics Platform

**Optimizing Unused Cargo Space with Rule-Based Matching & ML Reliability Scoring**

---

##  Problem Statement

Thousands of small exporters face **high logistics costs and shipment delays** because:

* Containers often depart **partially filled**
* Small consignments **cannot afford full-container bookings**
* Unused cargo space goes wasted
* Exporters overpay or wait longer for dedicated logistics

---

##  Solution Overview

**intelligent logistics backend platform** that:

* Discovers **unused cargo space in real time**
* Allows **partial container booking**
* Matches exporters with **nearby logistics providers**
* Uses **Machine Learning (XGBoost)** to rank options by **reliability**
* Ensures **safe & feasible routing using rule-based constraints**

 **Rule-based logic guarantees correctness**
 **ML optimizes reliability & decision quality**

---

##  Core Features Implemented

###  1. Route-Based Container Listing

Logistics providers list containers with:

* Origin & destination
* Departure date
* Total container capacity
* Already booked capacity
* Cost

---

###  2. Unused Space Detection (Rule-Based)

Unused space is computed as:

```
available_capacity = total_capacity - booked_capacity
```

Only containers with sufficient unused capacity are considered.

---

###  3. Two-Phase Matching Strategy

#### 🔹 Phase 1 – Rule-Based Filtering

Eliminates infeasible options by checking:

* Route compatibility
* Available capacity ≥ shipment size
* Valid departure date
* Cargo–container compatibility

> Ensures **correctness & safety**

---

#### 🔹 Phase 2 – ML-Based Ranking

Applies **XGBoost model** to:

* Predict on-time delivery probability
* Assign a **reliability score**
* Rank feasible containers

> Improves **decision quality without violating rules**

---

###  4. Partial Container Booking

Exporters can:

* Book only required space
* Pay proportionally
* Reduce cost
* Avoid unused space wastage

---

###  5. Reliability Optimization (ML)

* Trained on **Cargo-2000 dataset**
* Predicts probability of on-time delivery
* Used only **after rule-based filtering**

---

###  6. Recommendation Engine

Final ranking considers:

* Feasibility (rules)
* Reliability score (ML)
* Cost efficiency

---

###  7. Booking History

* Stores confirmed bookings
* Tracks exporter usage
* Enables analytics

---

###  8. Provider Dashboard

Logistics providers can view:

* Container utilization %
* Booked vs unused space
* Active routes

---

## 🏗️ System Architecture

```
┌──────────────┐
│   Exporter   │
└──────┬───────┘
       │ Shipment Request
       ▼
┌────────────────────┐
│ FastAPI Backend    │
│--------------------│
│ Rule-Based Engine  │─── Phase 1
│ ML Reliability     │─── Phase 2
│ Recommendation API │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│ PostgreSQL DB      │
│--------------------│
│ Containers         │
│ Bookings           │
│ Providers          │
└────────────────────┘

┌────────────────────┐
│ XGBoost ML Model   │
│ (Cargo-2000)       │
│ Reliability Score  │
└────────────────────┘
```

---

## Machine Learning Model (Reliability Engine)

### Dataset

* **Cargo-2000**
* Historical shipment delays & routing info

### Features Used

* Incoming leg departure delay
* Incoming leg receive delay
* Total route hops (complexity)

### Target

```
on_time = 1 if final_delivery_delay <= 0 else 0
```

### Output

```
Reliability Score = P(on-time delivery)
```

---

## 📡 API Endpoints Explained (with Examples)

---

### 🔹 1. Recommend Containers

**POST** `/recommend`

#### Request

```json
{
  "origin": "Chennai",
  "destination": "Hamburg",
  "required_capacity": 10
}
```

#### What happens internally

1. Rule-based filter checks:

   * Route match
   * Available capacity
2. ML model predicts reliability
3. Final score is computed
4. Containers are ranked

#### Response

```json
[
  {
    "container_id": 2,
    "available_capacity": 20,
    "reliability_score": 0.72,
    "cost": 1000,
    "final_score": 0.66
  }
]
```

---

### 🔹 2. View Unused Space

**GET** `/unused-space`

#### Response

```json
{
  "container_id": 1,
  "route": "Chennai → Hamburg",
  "utilization_percent": 33.33,
  "unused_capacity": 20
}
```

---

### 🔹 3. Book Container Space

**POST** `/book`

#### Request

```json
{
  "container_id": 2,
  "booked_capacity": 10
}
```

#### Result

* Capacity updated
* Booking stored
* History maintained

---

### 🔹 4. Booking History

**GET** `/bookings`

Shows all exporter bookings.

---

### 🔹 5. Provider Dashboard

**GET** `/provider/dashboard`

Displays:

* Container utilization
* Active routes
* Booking stats

---

## Database Design (PostgreSQL)

### Containers Table

* `id`
* `origin`
* `destination`
* `departure_date`
* `total_capacity`
* `booked_capacity`
* `cost`

### Bookings Table

* `id`
* `container_id`
* `booked_capacity`
* `timestamp`

---

##  Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL + SQLAlchemy
* **ML Model:** XGBoost
* **API Docs:** Swagger (OpenAPI)
* **Data:** Cargo-2000 Dataset

---

##  How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

##  Final Outcome

 Correct, rule-safe matching
 ML-powered reliability optimization
 Reduced logistics cost
 Real-time unused space utilization

