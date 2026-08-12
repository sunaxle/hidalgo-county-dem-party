const historicalVoterData = [
  // Primary Elections
  { year: 2006, type: "Primary Election", count: 271132 },
  { year: 2008, type: "Primary Election", count: 291301 },
  { year: 2012, type: "Primary Election", count: 293523 },
  { year: 2014, type: "Primary Election", count: 309275 },
  { year: 2016, type: "Primary Election", count: 317730 },
  { year: 2018, type: "Primary Election", count: 349735 },
  { year: 2020, type: "Primary Election", count: 379658 },
  { year: 2022, type: "Primary Election", count: 405377 },
  { year: 2024, type: "Primary Election", count: 431335 },
  // General Elections
  { year: 2008, type: "General Election", count: 284144 },
  { year: 2010, type: "General Election", count: 297602 },
  { year: 2012, type: "General Election", count: 307186 },
  { year: 2014, type: "General Election", count: 321564 },
  { year: 2016, type: "General Election", count: 338562 },
  { year: 2018, type: "General Election", count: 358850 },
  { year: 2020, type: "General Election", count: 391309 },
  { year: 2022, type: "General Election", count: 416978 },
  { year: 2024, type: "General Election", count: 434705 },
];

const voterRegistrationData = [
  { date: "2026-05-01", count: 458120 },
  { date: "2026-05-05", count: 458600 },
  { date: "2026-05-10", count: 459250 },
  { date: "2026-05-15", count: 460407 },
  { date: "2026-06-09", count: 461884 },
  { date: "2026-06-18", count: 462491 },
  { date: "2026-06-29", count: 463064 },
  { date: "2026-07-20", count: 463410 },
  { date: "2026-07-29", count: 463468 },
  { date: "2026-08-07", count: 463468 },
];

const voterRegistrationGoals = {
  baseline: 460407,
  lowGoal: 480000,
  highGoal: 500000,
  targetDate: "2026-10-05", // Typical October deadline
};
