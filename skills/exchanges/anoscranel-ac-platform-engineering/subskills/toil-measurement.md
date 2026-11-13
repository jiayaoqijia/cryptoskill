---
name: toil-measurement
domain: software-engineering/toil-measurement
trigger: "Measuring repetitive manual work to justify automating it."
anti_trigger: "Not for productivity scoring of individuals, and not for cost analysis."
scope: "Measuring repetitive work and the case for automating it."
status: seedling
---

# Toil measurement

## Standard

Toil is work that is manual, repetitive, automatable, and grows with the service rather than the team's judgment. The definition matters because it distinguishes toil from work that is manual but valuable — an incident diagnosis, a design review. Only the first should be automated, and only the first grows without bound if it is not.

Measuring it means counting rather than estimating. A team that logs the repetitive tasks it performs for two weeks produces a list with frequencies and durations, and that list supports a case: this task occurred forty times, took twenty minutes each, and would take three days to automate with a saving of eleven hours a month. Without the count, the case is an opinion competing with other opinions.

Primary sources: <https://sre.google/> and <https://sre.google/workbook/table-of-contents/>.

## Decision rules

- Record the task, its frequency, and its duration, measured over a stated period.
- Record whether the task grows with service count, traffic, or team size, since growth is what makes toil binding.
- Record the automation cost estimate and the payback period.
- Record the risk of automating badly, since a toil task with an exception path is often automated incorrectly.
- Record what percentage of the team's week the toil consumes.
- Record the tasks deliberately left manual and why.

## Procedure

1. Log repetitive tasks over a stated period with frequency and duration.
2. Record the growth driver for each.
3. Estimate automation cost and payback.
4. Rank by payback and by growth.
5. Record the tasks left manual and the reason.
6. Write the case with its arithmetic shown.

## Anti-patterns

- Estimating frequency from memory rather than counting.
- Automating a task that does not grow, where the saving is bounded.
- Ignoring the exception paths that make a toil task hard to automate well.
- Measuring toil by individual rather than by team, which turns a metric into a judgement.
- Automating a task that should be eliminated rather than automated.

## Done checklist

- [ ] Tasks logged with frequency and duration.
- [ ] Growth driver recorded.
- [ ] Automation cost and payback recorded.
- [ ] Risk of poor automation recorded.
- [ ] Team-level share recorded.
- [ ] Deliberately manual tasks recorded.

The measurement should also record who performs the task, since toil concentrated on one person is both a sustainability problem and a bus-factor problem, and automating it may matter more for the second reason than for the hours it saves.


## Sources

- Site reliability engineering on toil: <https://sre.google/>
- Operational practice: <https://sre.google/workbook/table-of-contents/>
- Automation guidance: <https://csrc.nist.gov/>
