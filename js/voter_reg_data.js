const historicalVoterData = [
  // Primary Elections
  { year: 2006, type: 'Primary Election', count: 271132 },
  { year: 2008, type: 'Primary Election', count: 291301 },
  { year: 2012, type: 'Primary Election', count: 293523 },
  { year: 2014, type: 'Primary Election', count: 309275 },
  { year: 2016, type: 'Primary Election', count: 317730 },
  { year: 2018, type: 'Primary Election', count: 349735 },
  { year: 2020, type: 'Primary Election', count: 379658 },
  { year: 2022, type: 'Primary Election', count: 405377 },
  { year: 2024, type: 'Primary Election', count: 431335 },
  // General Elections
  { year: 2008, type: 'General Election', count: 284144 },
  { year: 2010, type: 'General Election', count: 297602 },
  { year: 2012, type: 'General Election', count: 307186 },
  { year: 2014, type: 'General Election', count: 321564 },
  { year: 2016, type: 'General Election', count: 338990 },
  { year: 2018, type: 'General Election', count: 362952 },
  { year: 2020, type: 'General Election', count: 392604 },
  { year: 2022, type: 'General Election', count: 418169 },
  { year: 2024, type: 'General Election', count: 447359 }
];

const voterRegistrationData = [
  { date: '2026-05-01', count: 458120 },
  { date: '2026-05-05', count: 458600 },
  { date: '2026-05-10', count: 459250 },
  { date: '2026-05-15', count: 460407 }
];

const voterRegistrationGoals = {
  baseline: 460407,
  lowGoal: 480000,
  highGoal: 500000,
  targetDate: '2026-10-05' // Typical October deadline
};
