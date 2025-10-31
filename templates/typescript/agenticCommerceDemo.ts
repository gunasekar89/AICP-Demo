/**
 * Walmart-branded agentic commerce demo implemented in TypeScript.
 * Each agent is represented as a lightweight class mirroring the Python version
 * so teams can wire it into LangGraph/SWARM orchestrators.
 */

type ComboOffer = {
  name: string;
  items: Record<string, number>;
  totalPrice: number;
  savings: number;
  insights: string;
};

type StockAlert = {
  sku: string;
  currentLevel: number;
  forecastDemand: number;
  daysUntilStockout: number;
};

type SupplierOrder = {
  sku: string;
  orderQuantity: number;
  supplier: string;
  rationale: string;
};

type TicketSummary = {
  ticketId: string;
  synopsis: string;
  sentiment: string;
  nextAction: string;
};

type StrategyPacket = {
  executiveSummary: string;
  executionRoadmap: string[];
  quantumOutlook: string;
  memoryUpdates: Record<string, string>;
};

export class AgenticRetailAssistant {
  private weeklyCatalog: Record<string, number> = {
    "organic apples": 3.99,
    "oat milk": 5.49,
    "free-range eggs": 4.79,
    "sourdough bread": 4.25,
    avocado: 1.69,
    "almond butter": 7.99,
    quinoa: 6.5,
    "heirloom tomatoes": 4.1,
    spinach: 2.85,
    "greek yogurt": 6.25,
  };

  private partnerDiscounts: Record<string, number> = {
    farm_co: 0.1,
    dairy_collective: 0.08,
    artisan_bakery: 0.12,
  };

  public findBestCombos(audience: string, maxResults = 3): ComboOffer[] {
    const bundles: Array<[string, Record<string, number>]> = [
      [
        "Brunch Delight",
        { "sourdough bread": 1, avocado: 4, "free-range eggs": 1, "heirloom tomatoes": 3 },
      ],
      [
        "Wellness Glow",
        { "organic apples": 6, spinach: 2, quinoa: 1, "greek yogurt": 1 },
      ],
      [
        "Plant-Powered Pantry",
        { "oat milk": 2, "almond butter": 1, quinoa: 2, "organic apples": 4 },
      ],
    ];

    const premiumMultiplier = audience.toLowerCase().includes("premium") ? 1.05 : 1;
    const offers = bundles.map(([name, items]) => {
      const listPrice = Object.entries(items).reduce(
        (acc, [item, qty]) => acc + this.weeklyCatalog[item] * qty,
        0
      );
      const partnerDiscount = this.estimateDiscount(name);
      let adjustedPrice = listPrice * (1 - partnerDiscount);
      if (premiumMultiplier > 1) {
        adjustedPrice *= premiumMultiplier;
      }
      const savings = listPrice - adjustedPrice;
      return {
        name,
        items,
        totalPrice: Number(adjustedPrice.toFixed(2)),
        savings: Number(savings.toFixed(2)),
        insights: `Tailored for ${audience}. Partner discount: ${Math.round(
          partnerDiscount * 100
        )}%. Upsell cushion applied: ${premiumMultiplier.toFixed(2)}.`,
      } as ComboOffer;
    });

    return offers.sort((a, b) => b.savings - a.savings).slice(0, maxResults);
  }

  private estimateDiscount(bundleName: string): number {
    if (bundleName.includes("Brunch")) return this.partnerDiscounts.artisan_bakery;
    if (bundleName.includes("Wellness")) return this.partnerDiscounts.farm_co;
    return this.partnerDiscounts.dairy_collective;
  }
}

export class SmartInventoryAI {
  private leadTimes: Record<string, number> = { farm_co: 2, dairy_collective: 3, artisan_bakery: 1 };
  private dailyVelocity: Record<string, number> = {
    "organic apples": 18.0,
    "oat milk": 12.5,
    "free-range eggs": 22.0,
    "sourdough bread": 15.0,
    avocado: 30.0,
  };
  private currentStock: Record<string, number> = {
    "organic apples": 120,
    "oat milk": 48,
    "free-range eggs": 60,
    "sourdough bread": 40,
    avocado: 55,
  };

  public forecastLowStock(horizonDays = 7): StockAlert[] {
    const alerts: StockAlert[] = [];
    Object.entries(this.dailyVelocity).forEach(([sku, velocity]) => {
      const projectedDemand = Math.round(velocity * horizonDays);
      const currentLevel = this.currentStock[sku] ?? 0;
      const daysUntilStockout = velocity ? currentLevel / velocity : Infinity;
      if (projectedDemand >= currentLevel) {
        alerts.push({
          sku,
          currentLevel,
          forecastDemand: projectedDemand,
          daysUntilStockout: Number(daysUntilStockout.toFixed(1)),
        });
      }
    });
    return alerts.sort((a, b) => a.daysUntilStockout - b.daysUntilStockout);
  }

  public recommendSupplierOrders(alerts: StockAlert[]): SupplierOrder[] {
    return alerts.map((alert) => {
      const supplier = this.mapSupplier(alert.sku);
      const leadTime = this.leadTimes[supplier] ?? 2;
      const buffer = Math.max(Math.round(alert.forecastDemand * 0.2), 10);
      return {
        sku: alert.sku,
        orderQuantity: alert.forecastDemand + buffer,
        supplier,
        rationale: `Lead time ${leadTime} days. Adds ${buffer} units safety stock to cover demand spike and micro-fulfillment routing.`,
      };
    });
  }

  private mapSupplier(sku: string): string {
    if (["organic apples", "avocado"].includes(sku)) return "farm_co";
    if (["oat milk", "free-range eggs"].includes(sku)) return "dairy_collective";
    return "artisan_bakery";
  }
}

export class SupportCopilot {
  private topicKeywords: Record<string, string> = {
    checkout: "Payments Squad",
    delivery: "Fulfillment Ops",
    inventory: "Supply Chain",
    pricing: "Merchandising Analytics",
  };

  public summarise(ticketId: string, transcript: string): TicketSummary {
    const sentiment = this.detectSentiment(transcript);
    const owner = this.routeTicket(transcript);
    const synopsis = transcript.split(".")[0].trim();
    return {
      ticketId,
      synopsis,
      sentiment,
      nextAction: `Escalate to ${owner} with sentiment marker '${sentiment}'. Auto-generate status update for requester.`,
    };
  }

  private detectSentiment(transcript: string): string {
    const lower = transcript.toLowerCase();
    if (["angry", "frustrated", "urgent"].some((word) => lower.includes(word))) return "high negative";
    if (["thanks", "appreciate", "resolved"].some((word) => lower.includes(word))) return "positive";
    return "neutral";
  }

  private routeTicket(transcript: string): string {
    const lower = transcript.toLowerCase();
    for (const [keyword, squad] of Object.entries(this.topicKeywords)) {
      if (lower.includes(keyword)) return squad;
    }
    return "Central Support Pod";
  }
}

export class MultiAgentCommercePlanner {
  public composeStrategy(
    retailStory: string[],
    inventoryAlerts: string[],
    supportFocus: string
  ): StrategyPacket {
    const executiveSummary = `1. Retail: ${retailStory.join(" | ")}` +
      `\n2. Inventory: ${inventoryAlerts.join(" | ")}` +
      `\n3. Support: ${supportFocus}`;

    const executionRoadmap = [
      "• Discovery — Validate bundles with sentiment telemetry (Lead: Vision)",
      "• Creative Direction — Infuse brand voice across digital shelf (Lead: Brand)",
      "• Production — Automate fulfillment & support workflows (Lead: Fulfillment)",
    ];

    return {
      executiveSummary,
      executionRoadmap,
      quantumOutlook:
        "Quantum annealing sandbox models supplier and last-mile trade-offs in near real time, unlocking 18% faster decision cycles and adaptive shopper journeys.",
      memoryUpdates: {
        shared: "Sync combo uplift metrics to federated reinforcement learner.",
        support: "Flag recurring pricing signal drift for proactive knowledge updates.",
      },
    };
  }
}

export function runDemo(): void {
  const retailAssistant = new AgenticRetailAssistant();
  const inventoryAI = new SmartInventoryAI();
  const supportCopilot = new SupportCopilot();
  const planner = new MultiAgentCommercePlanner();

  const combos = retailAssistant.findBestCombos("Premium Walmart+ households");
  const alerts = inventoryAI.forecastLowStock();
  const orders = inventoryAI.recommendSupplierOrders(alerts);
  const ticket = supportCopilot.summarise(
    "TCK-48291",
    "Customer is frustrated that the fresh grocery delivery window keeps slipping. Mentions inventory gaps on avocados and expects proactive updates."
  );
  const strategy = planner.composeStrategy(
    combos.map((combo) => `${combo.name} saves $${combo.savings} for ${combo.insights}`),
    alerts.map((alert) => `${alert.sku} stockout in ${alert.daysUntilStockout}d`),
    ticket.nextAction
  );

  console.table(combos);
  console.table(alerts);
  console.table(orders);
  console.log(ticket);
  console.log(strategy);
}

if (require.main === module) {
  runDemo();
}
