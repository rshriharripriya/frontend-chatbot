#!/usr/bin/env python3

"""
Test API with Markdown Response
Returns properly formatted markdown for frontend testing
"""

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random
import json
from typing import List, Dict

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for frontend
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

@app.post("/query", response_model=QueryResponse)
async def query_route(payload: QueryRequest):
    user_input = payload.input
    await asyncio.sleep(2)  # simulate processing delay

    # Your sample markdown response
    markdown_output = """The comprehensive project health report has been generated with the following details:

# 📊 Project Health Report

## Executive Summary
This report provides an analysis of current project metrics and offers best practice recommendations to address identified areas for improvement. Our current project success rate is critically low at 9.00%, with significant challenges in cost overruns (average 43.2%) and schedule delays (average 25.6%). While no projects are currently classified as high-risk (Level 4-5), proactive risk management is essential.

## Current Project Metrics Analysis

### Overview
*   **Total Projects:** 300
*   **Successful Projects:** 27 (9.00%) - *Significantly below target*
*   **Average Team Size:** 15.5 people
*   **Average Complexity:** 3.0/5.0

### Cost Analysis
*   **Projects Over Budget (>15%):** 279
*   **Average Cost Overrun:** 43.2% - *High*
*   **Maximum Overrun:** 90.1%

### Schedule Analysis
*   **Delayed Projects (>30%):** 105
*   **Average Schedule Delay:** 25.6% - *High*
*   **Maximum Delay:** 50.2%

### Risk Assessment
*   **High-Risk Projects (Level 4-5):** 0 - *While currently zero, continuous vigilance and proactive management are crucial.*

### Top 5 Problem Projects
1.  **Project 45:** FAILED (Cost Overrun: 90.1%, Schedule Delay: 39.8%)
2.  **Project 55:** FAILED (Cost Overrun: 86.3%, Schedule Delay: 32.3%)
3.  **Project 212:** FAILED (Cost Overrun: 85.1%, Schedule Delay: 44.5%)
4.  **Project 138:** FAILED (Cost Overrun: 83.0%, Schedule Delay: 38.4%)
5.  **Project 183:** FAILED (Cost Overrun: 81.9%, Schedule Delay: 35.5%)

## Recommendations for Improvement

Based on project management best practices, the following recommendations are proposed to improve project success rates, reduce cost overruns, minimize schedule delays, and enhance risk management:

### 1. Improving Project Success Rate (Target: 85%+)
*   **Comprehensive Planning:** Implement rigorous planning processes including detailed task prioritization, scheduling, resource identification, budget setting, deliverable definition, quality targets, and communication plans.
*   **Stagger Project Phases:** For organizations managing multiple projects, strategically stagger project phases (Initiation, Planning, Execution, Control, Closure) to optimize resource allocation and prevent bottlenecks.
*   **Financial Stewardship & Continuous Improvement:** Emphasize careful resource management, budget adherence, and a culture of continuous improvement to enhance efficiency and affordability.
*   **Effective Communication:** Foster robust communication strategies using diverse methods to ensure all stakeholders are informed and aligned.
*   **Proactive Risk Management:** Integrate risk identification, prevention, and mitigation into all project phases to ensure project viability.

### 2. Reducing Cost Overruns
*   **Strict Budget Adherence:** Reinforce the importance of adhering to approved budgets through diligent financial stewardship and careful resource management.
*   **Planned Expenditure:** Ensure that detailed budget planning and expenditure forecasts are integral parts of the project planning process.
*   **Efficiency Focus:** Continuously seek opportunities to improve processes, reduce waste, and enhance efficiency to lower costs.

### 3. Minimizing Schedule Delays
*   **Detailed Scheduling & Swift Execution:** Develop highly detailed project schedules and prioritize swift, efficient execution of the project plan.
*   **Managing Tight Deadlines:**
    *   Proactively negotiate for deadline extensions when feasible.
    *   If extensions are not possible, immediately re-plan the project to assess the extent of lateness.
    *   For projects projected to be more than 10% late, explore options for additional resources to accelerate delivery.
*   **Staggering Phases (for multiple projects):** Utilize phase staggering to manage workload and prevent simultaneous demands on resources that can lead to delays.

### 4. Managing High-Risk Projects (Proactive Measures)
*   **Integrated Risk Management:** Embed risk identification, assessment, and mitigation strategies into every stage of project planning and execution.
*   **Contingency Planning:** Develop robust contingency plans for identified risks to ensure project viability even in the face of unforeseen challenges.
*   **Regular Risk Reviews:** Conduct regular reviews of potential risks, their likelihood, impact, and the effectiveness of mitigation strategies.

## Conclusion
The current project performance indicates a critical need for immediate intervention and the adoption of robust project management best practices. By implementing the recommended strategies, particularly focusing on comprehensive planning, financial discipline, efficient execution, and proactive risk management, we can significantly improve project success rates, reduce cost and schedule deviations, and foster a more predictable and successful project delivery environment.

The report has been saved and is ready for review at `reports/report_report_type_20251106_161225.md`."""
    return QueryResponse(
        output=markdown_output,
        timestamp=str(datetime.now().isoformat()),
        action_logged=True
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
