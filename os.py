import streamlit as st


def calculate_waiting_time(processes, burst_time):
    n = len(processes)
    waiting_time = [0] * n
    completion_time = [0] * n

    for i in range(1, n):
        completion_time[i] = completion_time[i - 1] + burst_time[i - 1]
        waiting_time[i] = completion_time[i] - processes[i][1]

        if waiting_time[i] < 0:
            waiting_time[i] = 0

    return waiting_time


def calculate_turnaround_time(processes, burst_time, waiting_time):
    n = len(processes)
    turnaround_time = [0] * n

    for i in range(n):
        turnaround_time[i] = burst_time[i] + waiting_time[i]

    return turnaround_time


def calculate_average_time(processes, burst_time):
    waiting_time = calculate_waiting_time(processes, burst_time)
    turnaround_time = calculate_turnaround_time(processes, burst_time, waiting_time)
    total_waiting_time = sum(waiting_time)
    total_turnaround_time = sum(turnaround_time)
    n = len(processes)
    average_waiting_time = total_waiting_time / n
    average_turnaround_time = total_turnaround_time / n

    return average_waiting_time, average_turnaround_time


def fcfs(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    return calculate_average_time(processes, burst_time)


def sjf(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    burst_time, processes = zip(*sorted(zip(burst_time, processes), key=lambda x: x[0]))
    return calculate_average_time(processes, burst_time)


def srtf(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    remaining_time = burst_time.copy()
    completion_time = 0
    processes_executed = 0
    waiting_time = [0] * n

    while processes_executed != n:
        min_time = float('inf')
        shortest = -1

        for i in range(n):
            if remaining_time[i] > 0 and remaining_time[i] < min_time:
                min_time = remaining_time[i]
                shortest = i

        if shortest == -1:
            completion_time += 1
            continue

        remaining_time[shortest] -= 1

        if remaining_time[shortest] == 0:
            processes_executed += 1
            waiting_time[shortest] = completion_time - processes[shortest][1] - burst_time[shortest]

        completion_time += 1

    return calculate_average_time(processes, burst_time)


def ljf(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    burst_time, processes = zip(*sorted(zip(burst_time, processes), key=lambda x: x[0], reverse=True))
    return calculate_average_time(processes, burst_time)


def lrtf(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    remaining_time = burst_time.copy()
    completion_time = 0
    processes_executed = 0
    waiting_time = [0] * n

    while processes_executed != n:
        max_time = 0
        longest = -1

        for i in range(n):
            if remaining_time[i] > 0 and remaining_time[i] > max_time:
                max_time = remaining_time[i]
                longest = i

        if longest == -1:
            completion_time += 1
            continue

        remaining_time[longest] -= 1

        if remaining_time[longest] == 0:
            processes_executed += 1
            waiting_time[longest] = completion_time - processes[longest][1] - burst_time[longest]

        completion_time += 1

    return calculate_average_time(processes, burst_time)


def priority_preemptive(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    priority = [p[2] for p in processes]
    remaining_time = burst_time.copy()
    completion_time = 0
    processes_executed = 0
    waiting_time = [0] * n

    while processes_executed != n:
        min_priority = float('inf')
        highest = -1

        for i in range(n):
            if remaining_time[i] > 0 and priority[i] < min_priority:
                min_priority = priority[i]
                highest = i

        if highest == -1:
            completion_time += 1
            continue

        remaining_time[highest] -= 1

        if remaining_time[highest] == 0:
            processes_executed += 1
            waiting_time[highest] = completion_time - processes[highest][1] - burst_time[highest]

        completion_time += 1

    return calculate_average_time(processes, burst_time)


def priority_non_preemptive(processes):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    priority = [p[2] for p in processes]
    burst_time, priority, processes = zip(*sorted(zip(burst_time, priority, processes), key=lambda x: x[2]))
    return calculate_average_time(processes, burst_time)


def round_robin(processes, quantum_time):
    n = len(processes)
    burst_time = [p[0] for p in processes]
    remaining_time = burst_time.copy()
    completion_time = 0
    processes_executed = 0
    waiting_time = [0] * n

    while processes_executed != n:
        for i in range(n):
            if remaining_time[i] > 0:
                if remaining_time[i] > quantum_time:
                    completion_time += quantum_time
                    remaining_time[i] -= quantum_time
                else:
                    completion_time += remaining_time[i]
                    waiting_time[i] = completion_time - processes[i][1] - burst_time[i]
                    remaining_time[i] = 0
                    processes_executed += 1

    return calculate_average_time(processes, burst_time)


def get_processes():
    processes = []
    n = st.number_input("Enter the number of processes", value=1, min_value=1, step=1)

    for i in range(n):
        burst_time = st.number_input(f"Enter the burst time for process {i + 1}", value=1, min_value=1, step=1)
        arrival_time = 0  # Assume all processes arrive at time 0 for simplicity
        priority = st.number_input(f"Enter the priority for process {i + 1}", value=1, min_value=1, step=1)
        processes.append((burst_time, arrival_time, priority))

    return processes


def main():
    st.title("CPU Scheduling Algorithms")
    processes = get_processes()

    algorithm_choice = st.selectbox("Select Scheduling Algorithm",
                                    ("First-Come, First-Served (FCFS)",
                                     "Shortest Job First (SJF)",
                                     "Shortest Remaining Time First (SRTF)",
                                     "Longest Job First (LJF)",
                                     "Longest Remaining Time First (LRTF)",
                                     "Priority (Preemptive)",
                                     "Priority (Non-Preemptive)",
                                     "Round Robin"))

    if algorithm_choice == "First-Come, First-Served (FCFS)":
        avg_waiting_time, avg_turnaround_time = fcfs(processes)
        st.subheader("FCFS Scheduling")
    elif algorithm_choice == "Shortest Job First (SJF)":
        avg_waiting_time, avg_turnaround_time = sjf(processes)
        st.subheader("SJF Scheduling")
    elif algorithm_choice == "Shortest Remaining Time First (SRTF)":
        avg_waiting_time, avg_turnaround_time = srtf(processes)
        st.subheader("SRTF Scheduling")
    elif algorithm_choice == "Longest Job First (LJF)":
        avg_waiting_time, avg_turnaround_time = ljf(processes)
        st.subheader("LJF Scheduling")
    elif algorithm_choice == "Longest Remaining Time First (LRTF)":
        avg_waiting_time, avg_turnaround_time = lrtf(processes)
        st.subheader("LRTF Scheduling")
    elif algorithm_choice == "Priority (Preemptive)":
        avg_waiting_time, avg_turnaround_time = priority_preemptive(processes)
        st.subheader("Priority (Preemptive) Scheduling")
    elif algorithm_choice == "Priority (Non-Preemptive)":
        avg_waiting_time, avg_turnaround_time = priority_non_preemptive(processes)
        st.subheader("Priority (Non-Preemptive) Scheduling")
    elif algorithm_choice == "Round Robin":
        quantum_time = st.number_input("Enter the time quantum for Round Robin", value=1, min_value=1, step=1)
        avg_waiting_time, avg_turnaround_time = round_robin(processes, quantum_time)
        st.subheader("Round Robin Scheduling")

    st.subheader("Average Waiting Time")
    st.write(avg_waiting_time)
    st.subheader("Average Turnaround Time")
    st.write(avg_turnaround_time)


if __name__ == '__main__':
    main()
