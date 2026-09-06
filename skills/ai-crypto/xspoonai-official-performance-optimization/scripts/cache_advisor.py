#!/usr/bin/env python3
"""
Cache Advisor
Recommends caching strategies for performance optimization
"""

import hashlib
from typing import Dict, List, Any, Optional
from enum import Enum

class CacheStrategy(Enum):
    """Cache strategies."""
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    FIFO = "fifo"
    ARC = "arc"

class CacheAdvisor:
    """Advises on caching strategies."""

    def __init__(self):
        self.strategies = {
            "lru": self._analyze_lru,
            "lfu": self._analyze_lfu,
            "ttl": self._analyze_ttl,
            "fifo": self._analyze_fifo,
            "arc": self._analyze_arc
        }

    def analyze_caching_opportunity(self, access_pattern: Dict) -> Dict[str, Any]:
        """Analyze if caching would help."""
        
        total_accesses = access_pattern.get("total_accesses", 0)
        unique_items = access_pattern.get("unique_items", 0)
        repeated_accesses = access_pattern.get("repeated_accesses", 0)
        
        if total_accesses == 0 or unique_items == 0:
            return {
                "status": "INVALID_DATA",
                "recommendation": "Provide valid access pattern data"
            }
        
        # Calculate metrics
        reuse_ratio = repeated_accesses / total_accesses
        unique_ratio = unique_items / total_accesses
        
        # Determine if caching is beneficial
        is_beneficial = reuse_ratio > 0.3 and unique_ratio < 0.8
        
        performance_gain = None
        if is_beneficial:
            # Estimate performance improvement
            cache_hit_rate = min(0.95, reuse_ratio + 0.2)
            performance_gain = cache_hit_rate * 80  # Up to 80% improvement
        
        return {
            "total_accesses": total_accesses,
            "unique_items": unique_items,
            "reuse_ratio": round(reuse_ratio, 2),
            "unique_ratio": round(unique_ratio, 2),
            "is_beneficial": is_beneficial,
            "estimated_gain_percent": round(performance_gain, 1) if performance_gain else 0,
            "recommended_strategies": self._recommend_strategies(reuse_ratio, unique_items),
            "implementation_complexity": "LOW" if is_beneficial else "N/A"
        }

    def recommend_cache_size(self, access_pattern: Dict, memory_budget_mb: int = 100) -> Dict[str, Any]:
        """Recommend cache size and strategy."""
        
        unique_items = access_pattern.get("unique_items", 0)
        avg_item_size_kb = access_pattern.get("avg_item_size_kb", 1)
        working_set_percent = access_pattern.get("working_set_percent", 80)
        
        # Calculate ideal cache size
        total_data_size = unique_items * avg_item_size_kb / 1024
        ideal_cache_size = (total_data_size * working_set_percent / 100)
        ideal_cache_size = min(ideal_cache_size, memory_budget_mb)
        
        # Calculate item capacity
        max_items = int((ideal_cache_size * 1024) / avg_item_size_kb)
        
        # Hit rate estimation
        if max_items >= unique_items:
            hit_rate = 0.95
        elif max_items >= (unique_items * working_set_percent / 100):
            hit_rate = 0.85
        else:
            hit_rate = (max_items / unique_items) * 0.8
        
        return {
            "total_data_size_mb": round(total_data_size, 2),
            "recommended_cache_size_mb": round(ideal_cache_size, 2),
            "max_items": max_items,
            "avg_item_size_kb": avg_item_size_kb,
            "estimated_hit_rate": round(hit_rate, 2),
            "memory_efficiency": round((ideal_cache_size / memory_budget_mb) * 100, 1),
            "recommendations": [
                f"Cache {max_items} items",
                f"Expected hit rate: {round(hit_rate*100, 1)}%",
                f"Memory usage: {round(ideal_cache_size, 1)}MB"
            ]
        }

    def compare_strategies(self, metrics: Dict) -> Dict[str, Any]:
        """Compare different caching strategies."""
        
        comparisons = {}
        
        for strategy_name, analyzer in self.strategies.items():
            comparisons[strategy_name] = analyzer(metrics)
        
        # Rank strategies
        ranked = sorted(
            comparisons.items(),
            key=lambda x: x[1].get("overall_score", 0),
            reverse=True
        )
        
        return {
            "strategies": comparisons,
            "ranked": [{"strategy": name, "score": data["overall_score"]} for name, data in ranked],
            "recommended": ranked[0][0] if ranked else None,
            "comparison": self._generate_comparison_table(comparisons)
        }

    def generate_cache_implementation(self, strategy: str, language: str = "python") -> str:
        """Generate cache implementation code."""
        
        implementations = {
            "python": {
                "lru": self._python_lru_cache(),
                "ttl": self._python_ttl_cache(),
                "lfu": self._python_lfu_cache()
            },
            "javascript": {
                "lru": self._js_lru_cache(),
                "ttl": self._js_ttl_cache()
            }
        }
        
        return implementations.get(language, {}).get(strategy, "# Not implemented")

    def analyze_cache_invalidation(self, access_pattern: Dict) -> Dict[str, Any]:
        """Analyze cache invalidation strategy needs."""
        
        data_freshness_seconds = access_pattern.get("data_freshness_seconds", 3600)
        update_frequency = access_pattern.get("update_frequency", "hourly")
        consistency_level = access_pattern.get("consistency_level", "eventual")
        
        strategies = {
            "TTL": {
                "description": "Time-based expiration",
                "suitable": data_freshness_seconds < 3600,
                "pros": ["Simple", "Predictable"],
                "cons": ["Stale data possible"],
                "ttl_seconds": max(60, data_freshness_seconds // 2)
            },
            "Event-Based": {
                "description": "Invalidate on data changes",
                "suitable": consistency_level == "strong",
                "pros": ["Always fresh", "Consistent"],
                "cons": ["Complex to implement"],
                "trigger": "On data update event"
            },
            "Hybrid": {
                "description": "TTL with event invalidation",
                "suitable": True,
                "pros": ["Balanced approach"],
                "cons": ["Medium complexity"],
                "parameters": {
                    "ttl_seconds": max(60, data_freshness_seconds // 2),
                    "invalidate_on_event": True
                }
            }
        }
        
        recommended = None
        if consistency_level == "strong":
            recommended = "Event-Based"
        elif data_freshness_seconds < 300:
            recommended = "TTL"
        else:
            recommended = "Hybrid"
        
        return {
            "data_freshness_seconds": data_freshness_seconds,
            "consistency_level": consistency_level,
            "strategies": strategies,
            "recommended": recommended,
            "recommendations": [
                f"Use {recommended} invalidation",
                "Monitor cache hit rate",
                "Alert on low hit rates"
            ]
        }

    # ===== Private Methods =====

    def _analyze_lru(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze LRU cache strategy."""
        return {
            "name": "LRU (Least Recently Used)",
            "description": "Evicts least recently used items",
            "memory_overhead": "LOW",
            "hit_rate": round(metrics.get("hit_rate", 0.8) * 0.95, 2),
            "time_complexity": "O(1)",
            "space_complexity": "O(n)",
            "best_for": "Working set fits in memory",
            "implementation": "dict + OrderedDict or collections.deque",
            "overall_score": 90
        }

    def _analyze_lfu(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze LFU cache strategy."""
        return {
            "name": "LFU (Least Frequently Used)",
            "description": "Evicts least frequently used items",
            "memory_overhead": "MEDIUM",
            "hit_rate": round(metrics.get("hit_rate", 0.8) * 0.92, 2),
            "time_complexity": "O(1) amortized",
            "space_complexity": "O(n)",
            "best_for": "Skewed access patterns",
            "implementation": "dict + heap + frequency map",
            "overall_score": 85
        }

    def _analyze_ttl(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze TTL cache strategy."""
        return {
            "name": "TTL (Time-To-Live)",
            "description": "Items expire after set time",
            "memory_overhead": "LOW",
            "hit_rate": round(metrics.get("hit_rate", 0.8) * 0.85, 2),
            "time_complexity": "O(1)",
            "space_complexity": "O(n)",
            "best_for": "Data with predictable staleness",
            "implementation": "dict + timestamps",
            "overall_score": 80
        }

    def _analyze_fifo(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze FIFO cache strategy."""
        return {
            "name": "FIFO (First-In-First-Out)",
            "description": "Evicts oldest items first",
            "memory_overhead": "VERY_LOW",
            "hit_rate": round(metrics.get("hit_rate", 0.8) * 0.7, 2),
            "time_complexity": "O(1)",
            "space_complexity": "O(n)",
            "best_for": "Simple use cases",
            "implementation": "deque",
            "overall_score": 70
        }

    def _analyze_arc(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze ARC cache strategy."""
        return {
            "name": "ARC (Adaptive Replacement Cache)",
            "description": "Adapts between LRU and LFU",
            "memory_overhead": "MEDIUM",
            "hit_rate": round(metrics.get("hit_rate", 0.8) * 0.96, 2),
            "time_complexity": "O(1) amortized",
            "space_complexity": "O(n)",
            "best_for": "Mixed workloads",
            "implementation": "Complex - multiple lists",
            "overall_score": 95
        }

    def _recommend_strategies(self, reuse_ratio: float, unique_items: int) -> List[str]:
        """Recommend caching strategies based on pattern."""
        recommendations = []
        
        if reuse_ratio > 0.7:
            recommendations.append("LRU - high temporal locality")
        elif unique_items > 10000:
            recommendations.append("LFU - frequency-based eviction")
        else:
            recommendations.append("TTL - time-based expiration")
        
        recommendations.append("ARC - adaptive hybrid approach")
        
        return recommendations

    def _generate_comparison_table(self, comparisons: Dict) -> str:
        """Generate comparison table."""
        lines = ["Strategy | Hit Rate | Memory | Complexity | Score"]
        lines.append("---------|----------|--------|------------|-------")
        
        for name, data in comparisons.items():
            line = f"{name:8} | {data.get('hit_rate', 0):.2f}   | {data.get('memory_overhead', '?'):8} | O(1)       | {data.get('overall_score', 0)}"
            lines.append(line)
        
        return "\n".join(lines)

    def _python_lru_cache(self) -> str:
        """Generate Python LRU cache implementation."""
        return '''from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
'''

    def _python_ttl_cache(self) -> str:
        """Generate Python TTL cache implementation."""
        return '''import time

class TTLCache:
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def put(self, key, value):
        self.cache[key] = (value, time.time())
'''

    def _python_lfu_cache(self) -> str:
        """Generate Python LFU cache implementation."""
        return '''class LFUCache:
    def __init__(self, capacity):
        self.cache = {}
        self.freq = {}
        self.min_freq = 0
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.freq[key] = self.freq.get(key, 0) + 1
        return self.cache[key]
    
    def put(self, key, value):
        if self.capacity <= 0:
            return
        if key in self.cache:
            self.cache[key] = value
            self.freq[key] += 1
            return
        if len(self.cache) >= self.capacity:
            min_key = min(self.cache, key=lambda k: self.freq[k])
            del self.cache[min_key]
        self.cache[key] = value
        self.freq[key] = 1
'''

    def _js_lru_cache(self) -> str:
        """Generate JavaScript LRU cache implementation."""
        return '''class LRUCache {
    constructor(capacity) {
        this.capacity = capacity;
        this.cache = new Map();
    }
    
    get(key) {
        if (!this.cache.has(key)) return -1;
        this.cache.delete(key);
        this.cache.set(key, this.cache.get(key));
        return this.cache.get(key);
    }
    
    put(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        }
        this.cache.set(key, value);
        if (this.cache.size > this.capacity) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
    }
}
'''

    def _js_ttl_cache(self) -> str:
        """Generate JavaScript TTL cache implementation."""
        return '''class TTLCache {
    constructor(ttlSeconds = 3600) {
        this.cache = new Map();
        this.ttl = ttlSeconds * 1000;
    }
    
    get(key) {
        if (!this.cache.has(key)) return null;
        const {value, timestamp} = this.cache.get(key);
        if (Date.now() - timestamp > this.ttl) {
            this.cache.delete(key);
            return null;
        }
        return value;
    }
    
    put(key, value) {
        this.cache.set(key, {value, timestamp: Date.now()});
    }
}
'''


if __name__ == "__main__":
    advisor = CacheAdvisor()
    
    # Test
    pattern = {
        "total_accesses": 10000,
        "unique_items": 500,
        "repeated_accesses": 7000
    }
    
    result = advisor.analyze_caching_opportunity(pattern)
    
    import json
    print(json.dumps(result, indent=2))
