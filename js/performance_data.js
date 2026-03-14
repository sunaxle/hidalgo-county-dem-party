// Generating realistic mock data for 103 Hidalgo County Precincts
const performanceData = [];

// Realistic ranges for Hidalgo County precincts
const MIN_VOTERS = 1500;
const MAX_VOTERS = 6000;
const PRIM_TURNOUT_MIN = 0.08; // 8% primary turnout
const PRIM_TURNOUT_MAX = 0.15; // 15% primary turnout
const MAX_PRECINCT = 110;

for (let i = 1; i <= MAX_PRECINCT; i++) {
    // Generate valid precinct (skipping some numbers if they don't exist, but we will just generate for all 1-110 for this mock)
    const registered = Math.floor(Math.random() * (MAX_VOTERS - MIN_VOTERS + 1)) + MIN_VOTERS;
    
    // Past primary performance is typically a fraction of registered voters
    const turnoutRate = (Math.random() * (PRIM_TURNOUT_MAX - PRIM_TURNOUT_MIN)) + PRIM_TURNOUT_MIN;
    const pastPrimary = Math.floor(registered * turnoutRate);
    
    // Target votes for general election (often based on previous general performance + growth goal)
    // Let's say target is broadly 35-50% of registered
    const targetRate = (Math.random() * (0.50 - 0.35)) + 0.35;
    const target = Math.floor(registered * targetRate);

    performanceData.push({
        precinct: i.toString(),
        registered_voters: registered,
        past_primary: pastPrimary,
        target_votes: target
    });
}
