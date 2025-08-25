// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

// Switch to the BTG Pactual database
db = db.getSiblingDB("btg_pactual");

// Create collections with validation
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "hashed_password", "full_name", "role", "is_active"],
      properties: {
        email: { bsonType: "string" },
        hashed_password: { bsonType: "string" },
        full_name: { bsonType: "string" },
        phone_number: { bsonType: "string" },
        role: { enum: ["admin", "client"] },
        is_active: { bsonType: "bool" },
        current_balance: { bsonType: "decimal" },
        notification_preference: { enum: ["email", "sms"] },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" },
      },
    },
  },
});

db.createCollection("funds", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "category", "minimum_amount"],
      properties: {
        name: { bsonType: "string" },
        description: { bsonType: "string" },
        category: { bsonType: "string" },
        minimum_amount: { bsonType: "decimal" },
        is_active: { bsonType: "bool" },
        created_at: { bsonType: "date" },
      },
    },
  },
});

db.createCollection("transactions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "type", "amount", "status"],
      properties: {
        user_id: { bsonType: "string" },
        fund_id: { bsonType: "string" },
        subscription_id: { bsonType: "string" },
        type: { enum: ["subscription", "cancellation"] },
        amount: { bsonType: "decimal" },
        status: { enum: ["pending", "completed", "failed"] },
        description: { bsonType: "string" },
        created_at: { bsonType: "date" },
        processed_at: { bsonType: "date" },
      },
    },
  },
});

db.createCollection("user_fund_subscriptions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "fund_id", "amount", "is_active"],
      properties: {
        user_id: { bsonType: "string" },
        fund_id: { bsonType: "string" },
        amount: { bsonType: "decimal" },
        is_active: { bsonType: "bool" },
        subscribed_at: { bsonType: "date" },
        cancelled_at: { bsonType: "date" },
      },
    },
  },
});

// Create indexes for better performance
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ role: 1 });
db.users.createIndex({ is_active: 1 });

db.funds.createIndex({ name: 1 });
db.funds.createIndex({ category: 1 });
db.funds.createIndex({ is_active: 1 });

db.transactions.createIndex({ user_id: 1 });
db.transactions.createIndex({ fund_id: 1 });
db.transactions.createIndex({ type: 1 });
db.transactions.createIndex({ status: 1 });
db.transactions.createIndex({ created_at: -1 });

db.user_fund_subscriptions.createIndex({ user_id: 1 });
db.user_fund_subscriptions.createIndex({ fund_id: 1 });
db.user_fund_subscriptions.createIndex(
  { user_id: 1, fund_id: 1 },
  { unique: true }
);
db.user_fund_subscriptions.createIndex({ is_active: 1 });

print("✅ BTG Pactual database initialized successfully!");
print(
  "📊 Collections created: users, funds, transactions, user_fund_subscriptions"
);
print("🔍 Indexes created for optimal performance");
print("🚀 Ready to receive data from the FastAPI application");
