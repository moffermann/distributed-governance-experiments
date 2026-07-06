# Questionnaire — Spanish

## Purpose

This questionnaire is designed for both:

```text
LLM synthetic calibration
future human survey / vignette study
```

It must be administered after showing `CONTEXT_BRIEF_ES.md`.

## Response scale

For probability questions, use values from `0` to `100`.

Later these are normalized into `[0, 1]`.

```text
0   = definitely not / never
25  = unlikely
50  = uncertain / about half the time
75  = likely
100 = almost certain / always
```

## Section 1 — Understanding check

1. In this scenario, are you being asked to donate extra money from your own pocket?

```text
Yes / No / Not sure
```

2. In this scenario, where does the money come from?

```text
A. Extra voluntary donations from citizens
B. Public funds / taxes already collected
C. Private company donations
D. Not sure
```

3. How easy is it to revoke delegation in the scenario?

```text
A. Requires paperwork at a municipal office
B. Requires a legal procedure
C. Can be done simply in the app, e.g. with one click
D. Not sure
```

Responses failing this section should be flagged, not automatically discarded.

## Section 2 — Citizen participation and delegation

4. If this application existed, how likely would you be to directly review public project priorities or projects at least occasionally?

```text
0-100
```

5. If you had little time, low interest, or low comfort using the app, how likely would you be to delegate your participation to someone else?

```text
0-100
```

6. If you delegated, whom would you most likely choose?

Allocate 100 points across options:

```text
family_member
partner_or_spouse
trusted_friend
trusted_neighbor
local_community_leader
technical_expert
public_institution_or_ngo
political_party_or_political_actor
public_influencer
would_not_delegate
```

7. How much would the fact that delegation can be revoked with one click increase your willingness to delegate?

```text
0-100
```

8. How much would visible reports of delegate actions increase your willingness to delegate?

```text
0-100
```

9. If your delegate supported priorities clearly different from what you expected, how likely would you be to review what happened?

```text
0-100
```

10. If your delegate repeatedly acted against your expectations, how likely would you be to revoke or change the delegate?

```text
0-100
```

11. If your delegate did not use the platform for a long time, how likely would you be to revoke or change the delegate?

```text
0-100
```

12. How likely would you be to read short notifications about what your delegate did?

```text
0-100
```

13. How likely would you be to read detailed reports about what your delegate did?

```text
0-100
```

## Section 3 — If acting as a delegate

Answer this section as if you accepted responsibility to represent one or more people in the app.

14. If other people delegated to you, how often would you use the platform during a planning cycle?

```text
0-100
```

15. If you were a delegate, what share of the planning priorities would you realistically review before acting?

```text
0-100
```

16. How much would knowing that your actions are visible to delegators affect your effort to act responsibly?

```text
0-100
```

17. How much would knowing that delegators can revoke with one click affect your effort to act consistently with their preferences?

```text
0-100
```

18. How aligned do you think your decisions would be with the preferences of someone close to you who delegated to you?

```text
0-100
```

19. How aligned do you think your decisions would be with a large number of people who delegated to you but do not know you personally?

```text
0-100
```

20. How likely would you be to write or provide a short explanation of your decisions if the app made it easy?

```text
0-100
```

## Section 4 — Friction and comprehension

21. How easy would this app feel compared with doing an in-person municipal paperwork process?

```text
0 = much harder than paperwork
50 = similar
100 = much easier than paperwork
```

22. How confident would you be that you understand what delegation means in this app?

```text
0-100
```

23. How confident would you be that you know how to revoke delegation in this app?

```text
0-100
```

24. How much assistance would you need from another person to use the app?

```text
0 = no assistance
100 = constant assistance
```

## Section 5 — Open explanation

25. Briefly explain why you would participate directly, delegate, or avoid using the app.

26. Briefly explain what would make you trust or distrust a delegate.

27. Briefly explain what would make you revoke a delegate.

## Variables derived from this questionnaire

The responses can be mapped to:

```text
directParticipationProbability
delegationProbability
preferredDelegateTypeDistribution
revocationEaseEffect
reportVisibilityEffect
reportReadProbability
revocationLikelihoodAfterMisalignment
revocationLikelihoodAfterInactivity
delegatePlatformUseRate
delegatePlanningCoverage
delegateResponsibilityEffect
delegateRevocationDisciplineEffect
alignmentWithCloseDelegator
alignmentWithImpersonalDelegators
delegateReportQualityWillingness
perceivedEaseOfUse
perceivedUnderstanding
needForAssistance
```
