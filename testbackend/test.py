#!/usr/bin/env python3
"""
Test API with REAL Processing Simulation
Uses actual work to simulate backend processing (not just sleep)
This allows skeleton loader to show while backend is busy
"""

import asyncio
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    input: str


class QueryResponse(BaseModel):
    output: str
    timestamp: str
    action_logged: bool


def simulate_rag_search(query: str):
    """
    Simulates RAG search with actual processing work
    This is NOT blocking - it's doing real computation
    """
    # Simulate vector search operations
    results = []
    for i in range(10):
        # Actual CPU work - not just sleeping
        result = sum([j ** 2 for j in range(10000)])  # CPU intensive
        results.append(f"Document {i}: {result}")
    time.sleep(10)  # Small delay between batches
    return results


def simulate_metrics_analysis(query: str):
    """
    Simulates database query and metrics calculation
    """
    metrics = {}
    for i in range(5):
        # Actual computation
        computation = sum([x ** 3 for x in range(5000)])  # CPU work
        metrics[f"metric_{i}"] = computation
        time.sleep(0.08)  # Small incremental delay
    return metrics


def simulate_report_generation():
    """
    Simulates report generation with actual work
    """
    report_sections = []
    for section in range(4):
        # Real processing
        processed = len(str(sum([i ** 2 for i in range(8000)])))
        report_sections.append(processed)
        time.sleep(0.06)
    return report_sections


@app.post("/query", response_model=QueryResponse)
async def query_route(payload: QueryRequest):
    """
    Simulates real backend processing:
    1. RAG search (takes time due to CPU work)
    2. Metrics analysis (takes time due to DB queries + computation)
    3. Report generation (takes time due to formatting)

    Frontend skeleton shows during ALL these operations!
    """
    user_input = payload.input
    start_time = time.time()

    # STEP 1: Simulate RAG search (0.5 seconds)
    print("[BACKEND] Starting RAG search...")
    rag_results = simulate_rag_search(user_input)
    print(f"[BACKEND] RAG search complete: {len(rag_results)} results")

    # STEP 2: Simulate metrics analysis (0.4 seconds)
    print("[BACKEND] Analyzing metrics...")
    metrics = simulate_metrics_analysis(user_input)
    print(f"[BACKEND] Metrics analysis complete")

    # STEP 3: Simulate report generation (0.24 seconds)
    print("[BACKEND] Generating report...")
    report_sections = simulate_report_generation()
    print(f"[BACKEND] Report generation complete")

    elapsed = time.time() - start_time
    print(f"[BACKEND] Total processing time: {elapsed:.2f} seconds")

    # Now return the response (frontend skeleton was visible entire time!)
    markdown_output = """### Project Health Report: Key Findings and Recommendations

#### Overview of Current Project Performance:

* **Total Projects:** 300
* **Successful Projects:** 27 (9.00%) - *Significantly below target*
* **Average Team Size:** 15.5 people
* **Average Complexity:** 3.0/5.0

#### Critical Areas for Improvement:

**Cost Overruns:**
* Projects Over Budget (>15%): 279
* Average Cost Overrun: 43.2% - *High impact on profitability*
* Maximum Overrun: 90.1%

**Schedule Delays:**
* Delayed Projects (>30%): 105
* Average Schedule Delay: 25.6% - *Impacts delivery and resource utilization*
* Maximum Delay: 50.2%

**Risk Assessment:**
* High-Risk Projects (Level 4-5): 0 - *While currently zero, proactive management is crucial*

#### Top 5 Problem Projects (Examples of Critical Failures):

1. **Project 45:** FAILED (Cost Overrun: 90.1%, Schedule Delay: 39.8%)
2. **Project 55:** FAILED (Cost Overrun: 86.3%, Schedule Delay: 32.3%)
3. **Project 212:** FAILED (Cost Overrun: 85.1%, Schedule Delay: 44.5%)
4. **Project 138:** FAILED (Cost Overrun: 83.0%, Schedule Delay: 38.4%)
5. **Project 183:** FAILED (Cost Overrun: 81.9%, Schedule Delay: 35.5%)

---

#### Recommendations for Improvement:

**1. Improving Project Success Rate (Target: 85%+):**

* **Comprehensive Planning:** Implement a rigorous planning phase for all projects
  * Detailed task prioritization and duration calculation
  * Creation of a robust project schedule
  * Accurate resource identification and allocation
  * Setting clear budgets and expenditure plans
  * Defining deliverables and quality targets
  * Establishing clear communication plans
  * Developing strategies for managing risks, changes, and issues

* **Effective Execution:** Emphasize swift and efficient execution of the well-defined project plan

* **Enhanced Communication:** Foster a culture of transparent and frequent communication
  * Regular meetings and stand-ups
  * Progress reports and status updates
  * Team collaboration tools and platforms

* **Proactive Risk Management:** Integrate risk identification, prevention, and mitigation as a core responsibility

**2. Reducing Cost Overruns (Current: 43.2%):**

* **Strict Budget Management:** Project managers must act as financial stewards
  * Detailed budget setting and expenditure planning during initiation
  * Continuous monitoring and control of project costs throughout the lifecycle
  * Implementing robust change control processes to prevent scope creep

* **Efficiency and Affordability Focus:** Encourage teams to continuously seek opportunities for:
  * Process improvements
  * Cost-saving measures
  * Efficient resource utilization

**3.Minimizing Schedule Delays (Current: 25.6%):**

* **Detailed Scheduling and Tracking:** Develop highly detailed project schedules
  * Clear milestones and dependencies
  * Real-time tracking using project management tools
  * Early identification of potential delays

* **Swift and Agile Execution:** Promote efficient execution and empower teams
  * Timely decision-making
  * Quick issue resolution
  * Flexible methodology adoption

* **Resource Optimization:** Ensure resources are adequately allocated
  * Prevent bottlenecks
  * For multiple projects: stagger phases to optimize resource availability
  * Prevent simultaneous peak demands on same resources

**4. Managing High-Risk Projects (Currently 0, but essential for future):**

* **Integrated Risk Management:** Embed proactive risk management into every stage
  * Early and continuous identification of potential risks
  * Comprehensive risk prevention and mitigation strategies
  * Establishing contingency plans

* **Regular Risk Reviews:** Conduct regular reviews of:
  * Potential risks
  * Likelihood and impact assessment
  * Effectiveness of mitigation strategies
  * Update risk registers continuously

---

#### Conclusion:

The current project performance indicates a **critical need for systemic improvements** in project management practices. By implementing comprehensive planning, rigorous budget and schedule control, enhanced communication, and proactive risk management, the organization can significantly improve its project success rate and overall operational efficiency.

**A comprehensive project health report, including strategic recommendations for improving success rates, reducing cost overruns, minimizing schedule delays, and managing risks, has been generated and saved to** `reports/report_project_health_20251106_152923.md`."""

    return QueryResponse(
        output=markdown_output,
        timestamp=str(datetime.now().isoformat()),
        action_logged=True
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
