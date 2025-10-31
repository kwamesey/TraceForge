# TraceForge 🔍  
**Distributed System Visualization Simulator**

I built TraceForge to show how distributed systems talk to each other behind the scenes.  
Instead of one API, this project spins up multiple **FastAPI microservices** (auth, payments, recommendations) and a central **trace collector** that visualizes how requests flow through the system.

---

## 💡 Why I Built It
I wanted to design something that looked like what real backend teams use — where multiple services pass requests, forward trace IDs, and report metrics to a central dashboard.

TraceForge was built to show off:
- **Service-to-service communication**
- **Trace propagation** (UUIDs across requests)
- **Distributed request flow visualization**
- **Async APIs and instrumentation**
- **Container orchestration (Docker Compose)**

---

## ⚙️ Architecture
```
Client → service-auth → service-payments → service-recommendations
             │                    │                    │
             └──────→→→ all send spans to →→→ trace-collector
```

**Flow summary:**  
1. Client hits `service-auth` → generates a trace ID.  
2. Auth calls Payments, which calls Recommendations.  
3. Each service forwards the same trace ID via HTTP headers.  
4. Each service sends timing info (“span”) to `trace-collector`.  
5. The collector displays all traces in a simple HTML dashboard.  

---

## 🚀 Run the Whole System

```bash
docker-compose up --build
```

Then open:
- `http://localhost:8000` → Trace dashboard  
- `http://localhost:8001/auth` → Start the trace  
- `http://localhost:8002/pay` → Payments service  
- `http://localhost:8003/recs` → Recommendations service  

Every request shows up in the dashboard with its trace ID, services involved, and latency.

---

## 🧰 Tech Stack
- **Python 3.11**
- **FastAPI** (for all services)
- **httpx** (for internal service calls)
- **Docker Compose**
- **HTMX / HTML Dashboard**

---

## 🧑‍💻 About Me
I’m **Kwame Sey**, a computer science student passionate about **backend systems, networking, and observability**.  
This project demonstrates my ability to design and orchestrate distributed systems, visualize trace data, and think like a backend engineer.

---

## 📜 License
MIT License — free to use, modify, or extend.
