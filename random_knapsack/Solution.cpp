typedef long double longdouble;

typedef long long longlong;

#ifndef KNAPSACK_IDENTIFIER_ORDERED_SACK_ITEM_TREE_HPP
#define KNAPSACK_IDENTIFIER_ORDERED_SACK_ITEM_TREE_HPP

#include <list>

#include <tuple>

#include <string>

#include <map>

#include <algorithm>

// #include "../tree/bbst/SplayTree.t.hpp"

// #include "PartialSolution.hpp"

// #include "SackItem.hpp"

// note - not calling init() after constructing will lead to a null pointer issue

// use construct() to avoid this issue

/*

template <typename K, typename V, typename L>
class SplayTree;

*/

class SackItem;

/*
template <typename K, typename V, typename L>
class STEntry;

template <typename K, typename V, typename L>
class STNode;
*/

class SackItem;

#include <memory>

using namespace std;

using Y = map<int, shared_ptr<SackItem>,
		function<bool(int, int)>>;

class IdentifierOrderedSackItemTree {
public:
	using U = IdentifierOrderedSackItemTree;
	/*
	virtual int key_transform(SackItem *x) override;
	virtual int comparator(SackItem *a, SackItem *b) override;
	*/
	static shared_ptr<IdentifierOrderedSackItemTree>
		construct(shared_ptr<list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>> entries);
	static void ponder(int n);
	shared_ptr<SackItem> findSackItem(int id_value);
	shared_ptr<SackItem> insertSackItem(shared_ptr<SackItem> sack_item);
	void removeSackItem(int id_value);
	shared_ptr<list<shared_ptr<SackItem>>> toIdentifierOrderedSackItemList();
	virtual shared_ptr<U> clone();
	// virtual shared_ptr<BinaryTree<BSTEntry<SackItem, SackItem, int>>> _createTree() override;
	// virtual void init() override;
	IdentifierOrderedSackItemTree();
	virtual ~IdentifierOrderedSackItemTree();
protected:
	shared_ptr<Y> id_value_to_sack_item_map;
};

#include <string>

#include <cstdio>

#include <cstdlib>

#include <memory>

#include <list>

#include <algorithm>

#include <iostream>

using namespace std;

/*

template <typename K, typename V>
using U = tuple<shared_ptr<K>, shared_ptr<V>>;

*/

namespace Util {

string intToString(int a);

string longdoubleToString(longdouble a);

string longlongToString(longlong a);

shared_ptr<tuple<shared_ptr<int>, shared_ptr<int>>>
	makeIntSharedPtrTuple(int a, int b);

int comp(longdouble x, longdouble y);

shared_ptr<list<shared_ptr<int>>>
	removeDuplicateValuesGivenSortedValues(shared_ptr<list<shared_ptr<int>>> values);

shared_ptr<list<shared_ptr<int>>>
	removeDuplicateValuesGivenSortedValuesHelper(shared_ptr<list<shared_ptr<int>>> values,
		shared_ptr<int> prev_value, shared_ptr<list<shared_ptr<int>>> unique_values);

void ponder(int n);

}

#include <string>

#include <cmath>

#include <memory>

using namespace std;

class SackItem {
public:
	longlong getProfit();
	int getWeight();
	int getIDValue();
	void setProfit(longlong profit);
	void setWeight(int weight);
	void setIDValue(int identifier_value);
	longdouble getProfitWeightRatio();
	longdouble getLossValue(shared_ptr<SackItem> split_sack_item, bool is_included);
	shared_ptr<string> toString();
	SackItem(longlong profit, int weight, int id_value);
	~SackItem();
protected:
	longlong profit;
	int weight;
	int id_value;
};

#include <list>

#include <unordered_map>

#include <string>

#include <functional>

#include <utility>

#include <set>

// #include "BreakPartialSolution.hpp"

// #include "IdentifierOrderedSackItemTree.t.hpp"

// #include "SackItem.hpp"

class BreakPartialSolution;

class SackItem;

class SackProblem;

class PartialSolutionPathLabel;

class IdentifierOrderedSackItemTree;

class PostListDecomposeSubproblem;

using U = IdentifierOrderedSackItemTree;

using namespace std;

class PartialSolution : public enable_shared_from_this<PartialSolution> {
public:
	using B = BreakPartialSolution;
	using P = PartialSolution;
	static shared_ptr<P> construct(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			shared_ptr<SackItem> split_sack_item,
			shared_ptr<B> break_partial_solution,
			longdouble base_loss_value,
			shared_ptr<list<shared_ptr<P>>> constituent_partial_solutions);
	static shared_ptr<P> _combinePartialSolutions(shared_ptr<P> partial_solution1,
			shared_ptr<P> partial_solution2, shared_ptr<SackItem> split_sack_item,
			shared_ptr<B> break_partial_solution, shared_ptr<SackProblem> problem1,
			shared_ptr<SackProblem> problem2);
	shared_ptr<list<shared_ptr<PartialSolution>>> getConstituentPartialSolutions();
	shared_ptr<IdentifierOrderedSackItemTree> _getIdentifierOrderedSackItemTree();
	shared_ptr<list<shared_ptr<SackItem>>> getSackItems();
	shared_ptr<SackItem> _getSplitSackItem();
	longlong getTotalProfit();
	int getTotalWeight();
	longdouble getBaseLossValue();
	longdouble getNonBaseLossValue();
	longdouble getTotalLossValue();
	void setTotalProfit(longlong profit);
	void setTotalWeight(int weight);
	void setNonBaseLossValue(longdouble loss_value);
	void addSackItem(shared_ptr<SackItem> item, shared_ptr<BreakPartialSolution> break_partial_solution);
	void undoAddSackItem(shared_ptr<SackItem> break_partial_solution_sack_item);
	shared_ptr<PartialSolution> clone(shared_ptr<BreakPartialSolution> break_partial_solution);
	void addSackItems(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			shared_ptr<BreakPartialSolution> break_partial_solution);
	bool isFeasible(int capacity);
	shared_ptr<string> toString();
	shared_ptr<string> toBareString(shared_ptr<PostListDecomposeSubproblem>
			post_list_decompose_subproblem,
			shared_ptr<BreakPartialSolution> break_partial_solution);
	shared_ptr<string> toExtendedString();
	bool hasSackItem(shared_ptr<SackItem> sack_item);
	int getNumSackItems();
	shared_ptr<list<shared_ptr<SackItem>>> getItemsOrderedByIdentifierValue();
	shared_ptr<PartialSolutionPathLabel> toPartialSolutionPathLabel();
	PartialSolution(shared_ptr<SackItem> split_sack_item,
			shared_ptr<list<shared_ptr<PartialSolution>>> constituent_partial_solutions);
	~PartialSolution();
	int sack_item_count;
protected:
	shared_ptr<SackItem> split_sack_item;
	shared_ptr<list<shared_ptr<PartialSolution>>> constituent_partial_solutions;
	longdouble base_loss_value;
	longlong total_profit;
	int total_weight;
	longdouble non_base_loss_value;
	// note that we are not using reference_wrapper;
	// each instance of class for key
	// has its own count
	// unordered_map<SackItem *, int *> *sack_item_to_count_dict = new unordered_map<SackItem *, int *>(5);
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict;
	shared_ptr<IdentifierOrderedSackItemTree> identifier_ordered_sack_item_tree;
};

#include <list>

#include <algorithm>

// #include "PartialSolution.hpp"

using namespace std;

class PartialSolution;

class BreakPartialSolution;

using P = PartialSolution;
using B = BreakPartialSolution;

class BreakPartialSolution : public PartialSolution {
public:
	// used for creating a partial solution
	static shared_ptr<BreakPartialSolution> construct(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			shared_ptr<SackItem> split_sack_item);
	static shared_ptr<P> constructPartialSolution(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			shared_ptr<SackItem> split_sack_item,
			shared_ptr<B> break_partial_solution,
			longdouble base_loss_value,
			shared_ptr<list<shared_ptr<P>>> constituent_partial_solutions);
	static shared_ptr<P> _combinePartialSolutions(shared_ptr<P> partial_solution1,
			shared_ptr<P> partial_solution2, shared_ptr<SackItem> split_sack_item,
			shared_ptr<B> break_partial_solution, shared_ptr<SackProblem> problem1,
			shared_ptr<SackProblem> problem2);
	shared_ptr<PartialSolution> clone(shared_ptr<BreakPartialSolution> break_partial_solution);
	BreakPartialSolution(shared_ptr<SackItem> split_sack_item);
	~BreakPartialSolution();
};

#include <memory>

// #include "BreakPartialSolution.hpp"
// #include "SackProblem.hpp"
// #include "../feed_optimizer/Solution.t.hpp"
// #include "PartialSolution.hpp"

// #include "../util/Util.hpp"

// #include "SackItem.hpp"

// forward declaration
class PartialSolution;

class PartialSolutionPathLabel : public enable_shared_from_this<PartialSolutionPathLabel> {
	using A = PartialSolutionPathLabel;
public:
	static int comp(shared_ptr<A> a, shared_ptr<A> b);
	static int compHelper(shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items1,
			shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items2);
	static shared_ptr<A> getMin(shared_ptr<list<shared_ptr<A>>> partial_solution_path_labels);
	static shared_ptr<A> getMinHelper(shared_ptr<list<shared_ptr<A>>> partial_solution_path_labels,
			shared_ptr<A> curr_min);
	static shared_ptr<A> _combinePathLabels(shared_ptr<A> path_label1, shared_ptr<A> path_label2,
			shared_ptr<SackItem> split_sack_item,
			shared_ptr<BreakPartialSolution> break_partial_solution,
			shared_ptr<SackProblem> problem1, shared_ptr<SackProblem> problem2);
	shared_ptr<PartialSolution> _getPartialSolution();
	shared_ptr<list<shared_ptr<SackItem>>> _getSortedSackItems();
	bool isEqualTo(shared_ptr<A> path_label);
	PartialSolutionPathLabel(shared_ptr<PartialSolution> partial_solution);
	~PartialSolutionPathLabel();
protected:
	weak_ptr<PartialSolution> partial_solution;
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items;
};

#include <list>

#include <tuple>

// #include "problems/NonCoreSackSubproblem.hpp"
// #include "problems/PostListDecomposeSubproblem.hpp"
// #include "PartialSolution.hpp"
// #include "PartialSolutionPathLabel.hpp"

// #include "../dictionary/Dictionary.t.hpp"

class PartialSolution;

class NonCoreSackSubproblem;

using namespace std;

class ListDecomposition {
public:
	using P = PartialSolution;
	using A = PartialSolutionPathLabel;
	static void ponder(int n);
	static shared_ptr<list<shared_ptr<list<shared_ptr<P>>>>>
		groupByWeight(shared_ptr<list<shared_ptr<P>>> partial_solutions);
	static shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>,
		shared_ptr<A>>>>> getMaxScoreValuesGivenMaxWeight(shared_ptr<list<shared_ptr<P>>>
				partial_solutions, shared_ptr<NonCoreSackSubproblem> non_core_subproblem);
	static shared_ptr<list<shared_ptr<int>>>
		getResidualCapacitiesGivenPartialSolutions(shared_ptr<list<shared_ptr<P>>>
				partial_solutions, int capacity);
	static shared_ptr<list<shared_ptr<int>>>
		getClosestFeasibleWeightValuesGivenResidualCapacities(shared_ptr<list<shared_ptr<int>>>
				residual_capacities, shared_ptr<list<shared_ptr<int>>> weight_values);
	static shared_ptr<list<shared_ptr<int>>>
		getClosestFeasibleWeightValuesGivenResidualCapacitiesHelper(shared_ptr<list<shared_ptr<int>>>
				residual_capacities, shared_ptr<list<shared_ptr<int>>> weight_values,
				int prev_weight_value, shared_ptr<list<shared_ptr<int>>> closest_feasible_weight_values);

	// make sure that empty partial solution is a choice
	// for left and right partial solution lists
	static shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>>
		getABestPair(shared_ptr<list<shared_ptr<P>>> left_partial_solutions,
			shared_ptr<list<shared_ptr<P>>> right_partial_solutions, int capacity,
			shared_ptr<NonCoreSackSubproblem> non_core_subproblem,
			shared_ptr<PostListDecomposeSubproblem> left_problem,
			shared_ptr<PostListDecomposeSubproblem> right_problem);
};

#include <list>

#include <iostream>

#include <algorithm>

// #include "SackItem.hpp"

// #include "PartialSolution.hpp"

using namespace std;

class FractionalKnapsack {
public:
	static void ponder(int n);
	static shared_ptr<longdouble> quickSelect(shared_ptr<list<shared_ptr<longdouble>>> S, int k);
	static shared_ptr<longdouble> getMedian(shared_ptr<list<shared_ptr<longdouble>>> items);
	static shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>
		getWeightedMedian(shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> items, int W);
	static shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>, shared_ptr<SackItem>, shared_ptr<longdouble>>>
		linearTimeFractionalSolve(shared_ptr<list<shared_ptr<SackItem>>> items,
			int capacity);
	static shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<longdouble>>>
		toFractionalSolutionProfitAndWeightTuple(shared_ptr<PartialSolution> partial_solution,
				shared_ptr<SackItem> split_item, longdouble split_item_fraction);
};

#include <list>

#include <algorithm>

#include <memory>

using namespace std;

class IntegralityGapEstimate {
public:
	longdouble getOptimalFractionalSolutionProfit();
	longlong getBestIntegerSolutionProfit();
	void setBestIntegerSolutionProfit(longlong profit_value);
	longdouble getValue();
	void updateBestIntegerSolutionProfit(longlong integer_solution_profit);
	IntegralityGapEstimate(longdouble optimal_fractional_solution_profit,
			longlong best_integer_solution_profit);
	~IntegralityGapEstimate();
protected:
	longdouble optimal_fractional_solution_profit;
	longlong best_integer_solution_profit;
};

#endif

#ifndef FEED_OPTIMIZER_EVENTS_EVENT_HPP
#define FEED_OPTIMIZER_EVENTS_EVENT_HPP

// #include "../dictionary/Dictionary.hpp"

// #include "FeedItem.hpp"

// #include "FeedProblem.hpp"

#include <memory>

template <typename A, typename B>
class Dictionary;

class FeedItem;

using namespace std;

class Event {
public:
	virtual int getTime();
	virtual void handle(shared_ptr<Dictionary<int, FeedItem>> item_collection);
	virtual shared_ptr<string> toString();
	virtual bool isSolveEvent();
protected:
	Event(int time);
	virtual ~Event();
	int time;
};

// #include "Event.hpp"

class ItemEvent : public Event {
public:
	virtual shared_ptr<FeedItem> getItem();
protected:
	ItemEvent(int time, shared_ptr<FeedItem> item);
	virtual ~ItemEvent();
	shared_ptr<FeedItem> item;
};

#include <string>

#include <algorithm>

// #include "ItemEvent.hpp"

// #include "../dictionary/Dictionary.t.hpp"

using namespace std;

class ItemExpireEvent : public ItemEvent {
public:
	virtual shared_ptr<string> toString() override;
	void handle(shared_ptr<Dictionary<int, FeedItem>> item_collection);
	ItemExpireEvent(int time, shared_ptr<FeedItem> item);
	~ItemExpireEvent();
};

#include <string>

#include <algorithm>

// #include "ItemEvent.hpp"

// #include "../dictionary/Dictionary.t.hpp"

using namespace std;

class ItemIntroduceEvent : public ItemEvent {
public:
	virtual shared_ptr<string> toString() override;
	void handle(shared_ptr<Dictionary<int, FeedItem>> item_collection);
	ItemIntroduceEvent(int time, shared_ptr<FeedItem> item);
	~ItemIntroduceEvent();
};

#include <string>

#include <algorithm>

// #include "ItemEvent.hpp"

// #include "FeedItem.hpp"

// #include "../dictionary/Dictionary.t.hpp"

using namespace std;

class ItemTimeSpanningEvent : public ItemEvent {
public:
	virtual shared_ptr<string> toString() override;
	void handle(shared_ptr<Dictionary<int, FeedItem>> item_collection);
	ItemTimeSpanningEvent(int time, shared_ptr<FeedItem> item);
	~ItemTimeSpanningEvent();
};

#include <string>

#include <algorithm>

// #include "Event.hpp"

// #include "FeedProblem.hpp"

// #include "FeedOptimizer.hpp"

// #include "../dictionary/Dictionary.t.hpp"

using namespace std;

class SolveEvent : public Event {
public:
	int _getSackCapacity();
	shared_ptr<string>toString();
	void handle(shared_ptr<Dictionary<int, FeedItem>> item_collection);
	virtual bool isSolveEvent() override;
	SolveEvent(int time, int sack_capacity);
	~SolveEvent();
protected:
	int sack_capacity;
};

#include <unordered_map>

#include <list>

#include <tuple>

#include <string>

#include <iostream>

#include <functional>

#include <memory>

// #include "DictionaryDereferenceHash.t.hpp"

// #include "DictionaryDereferenceKeyEqual.t.hpp"

using namespace std;

template <typename A>
using H = function<size_t(const shared_ptr<A> a)>;

template <typename A>
using K = function<bool(const shared_ptr<A> a, const shared_ptr<A> b)>;

template <typename A>
size_t hash_fn(const shared_ptr<A> a) {
	shared_ptr<hash<A>> our_hash = shared_ptr<hash<A>>(new hash<A>());
	size_t result = (*our_hash)(*a);
	return result;
}

template <typename A>
bool key_equal_fn(const shared_ptr<A> a, const shared_ptr<A> b) {
	return *a == *b;
}

template <typename A, typename B>
class Dictionary {
	using M = unordered_multimap<shared_ptr<A>, shared_ptr<B>, H<A>, K<A>>;
public:
	static void ponder(int n);
	int getSize();
	bool isEmpty();
	shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> find(shared_ptr<A> k);
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> findAll(shared_ptr<A> k);
	void insert(shared_ptr<A> k, shared_ptr<B> v);
	void remove(shared_ptr<tuple<shared_ptr<A> , shared_ptr<B>>> e);
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> entries();
	shared_ptr<string> toString();
	Dictionary();
	~Dictionary();
protected:
	shared_ptr<M> _getEntryMap();
	shared_ptr<M> entry_map;
	int size;
};

#include <list>

#include <string>

#include <memory>

// #include "DoublyLinkedListNode.t.hpp"

template <typename E>
class DoublyLinkedListNode;

using namespace std;

template <typename E>
class DoublyLinkedList {
public:
	using N_l = DoublyLinkedListNode<E>;
	static shared_ptr<N_l> _createNode(shared_ptr<E> item, shared_ptr<N_l> prev, shared_ptr<N_l> next);
	static void ponder(int n);
	shared_ptr<N_l> _getHeaderSentinel();
	shared_ptr<N_l> _getTrailerSentinel();
	int getSize();
	bool isEmpty();
	void addBefore(shared_ptr<N_l> v, shared_ptr<N_l> z);
	void addAfter(shared_ptr<N_l> v, shared_ptr<N_l> z);
	void remove(shared_ptr<N_l> v);
	void addFirst(shared_ptr<N_l> v);
	void addLast(shared_ptr<N_l> v);
	shared_ptr<N_l> getFirst();
	shared_ptr<N_l> getLast();
	bool hasPredecessor(shared_ptr<N_l> node);
	bool hasSuccessor(shared_ptr<N_l> node);
	shared_ptr<list<shared_ptr<E>>> toElementList();
	shared_ptr<list<shared_ptr<E>>> _toElementListHelper(shared_ptr<N_l> node,
			shared_ptr<list<shared_ptr<E>>> partial_element_list);
	shared_ptr<list<shared_ptr<N_l>>> _toNodeList();
	shared_ptr<list<shared_ptr<N_l>>> _toNodeListHelper(shared_ptr<N_l> node,
			shared_ptr<list<shared_ptr<N_l>>> partial_node_list);
	shared_ptr<string> toString();
	DoublyLinkedList();
	~DoublyLinkedList();
protected:
	shared_ptr<N_l> header;
	shared_ptr<N_l> trailer;
	int size = 0;

};

#include <memory>

#include <iostream>

template <typename E>
class DoublyLinkedList;

using namespace std;

template <typename E>
class DoublyLinkedListNode {
	using N_l = DoublyLinkedListNode<E>;
public:
	shared_ptr<E> getElement();
	shared_ptr<N_l> getPrev();
	shared_ptr<N_l> getNext();
	void setElement(shared_ptr<E> element);
	void setPrev(shared_ptr<N_l> prev);
	void setNext(shared_ptr<N_l> next);
	DoublyLinkedListNode(shared_ptr<E> element, shared_ptr<N_l> prev, shared_ptr<N_l> next);
	~DoublyLinkedListNode();
protected:
	shared_ptr<E> element;
	shared_ptr<N_l> prev;
	shared_ptr<N_l> next;
};

#include <queue>

#include <functional>

// #include "../feed_optimizer/Event.hpp"

using namespace std;

/*

class EventTimeAscendingComparator {
public:
	static bool _comparator(Event *a, Event *b);
};

*/

class EventPriorityQueue {
	/*
	using Q = priority_queue<Event *, vector<Event *>,
			decltype(EventTimeAscendingComparator::_comparator)>;
	*/
	using Q = priority_queue<shared_ptr<Event>, vector<shared_ptr<Event>>,
			function<bool(shared_ptr<Event>, shared_ptr<Event>)>>;
public:
	static void ponder(int n);
	void pushEvent(shared_ptr<Event> event);
	shared_ptr<Event> popEvent();
	bool isEmpty();
	shared_ptr<Event> peek();
	EventPriorityQueue();
	~EventPriorityQueue();
protected:
	static bool _comparator(shared_ptr<Event> a, shared_ptr<Event> b);
	shared_ptr<Q> _getPriorityQueue();
	shared_ptr<Q> pqueue;
};

#include <string>

#include <memory>

using namespace std;

class FeedItem {
public:
	longlong getProfit();
	int getWeight();
	int getIDValue();
	shared_ptr<string> toString();
	FeedItem(longlong profit, int weight, int id_value);
	~FeedItem();
protected:
	longlong profit;
	int weight, id_value;
};

#include <list>

#include <tuple>

#include <algorithm>

#include <unordered_map>

// #include "FeedItem.hpp"

// #include "../knapsack/SackItem.hpp"

// #include "../knapsack/PartialSolution.hpp"

// #include "../knapsack/IdentifierOrderedSackItemTree.hpp"

// #include "../knapsack/FractionalKnapsack.hpp"

// #include "../knapsack/BreakPartialSolution.hpp"

// #include "../knapsack/PartialSolution.hpp"

// #include "../knapsack/problems/OriginalSackProblem.hpp"

// #include "../knapsack/SackProblem.hpp"

using namespace std;

class FeedProblem {
public:
	static shared_ptr<longlong> _getMaxItemProfit(shared_ptr<list<shared_ptr<FeedItem>>> items);
	static shared_ptr<int> _getMaxItemWeight(shared_ptr<list<shared_ptr<FeedItem>>> items);
	shared_ptr<list<shared_ptr<FeedItem>>> getItems();
	int _getSackCapacity();
	shared_ptr<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>, shared_ptr<longlong>>> solve();
	FeedProblem(shared_ptr<list<shared_ptr<FeedItem>>> feed_items, int capacity);
	~FeedProblem();
protected:
	shared_ptr<list<shared_ptr<FeedItem>>> items;
	int sack_capacity;
};

#include <tuple>

#include <list>

#include <algorithm>

// #include "FeedProblem.hpp"

class FeedProblem;

using namespace std;

class FeedOptimizer {
public:
	static shared_ptr<FeedProblem> transformForMinimizingSolutionSize(shared_ptr<FeedProblem> problem);
	static shared_ptr<tuple<shared_ptr<list<shared_ptr<FeedItem>>>, shared_ptr<longlong>>>
		untransformForMinimizingSolutionSize(shared_ptr<FeedProblem> original_problem,
			shared_ptr<FeedProblem> problem, shared_ptr<list<shared_ptr<FeedItem>>> item_collection,
			longlong total_profit);
};

#include <unordered_map>

#include <memory>

// #include "../feed_optimizer/Solution.t.hpp"

// #include "../list/DoublyLinkedList.hpp"
// #include "../../list/DoublyLinkedListNode.hpp"

// #include "BreakPartialSolution.hpp"

// #include "../knapsack/PartialSolution.hpp"

// #include "../knapsack/IdentifierOrderedSackItemTree.hpp"

class SackSubproblem;

template <typename E>
class DoublyLinkedListNode;

template <typename E>
class DoublyLinkedList;

class SackProblem : public enable_shared_from_this<SackProblem> {
public:
	using S = SackItem;
	using N = DoublyLinkedListNode<S>;
	using L = DoublyLinkedList<S>;
	shared_ptr<unordered_map<shared_ptr<S>, shared_ptr<int>>> _getSackItemToCountDict();
	virtual shared_ptr<list<shared_ptr<S>>> getSackItems();
	shared_ptr<list<shared_ptr<S>>> getSackItemsOrderedByLossValue();
	int getCapacity();
	void setCapacity(int capacity);
	int getNumSackItems();
	shared_ptr<BreakPartialSolution> _getBreakPartialSolution();
	shared_ptr<S> _getSplitSackItem();
	shared_ptr<S> getSackItemWithLowestLossValue();
	void addSackItemWithLargeLossValue(shared_ptr<S> sack_item);
	void removeSackItemWithLowestLossValue();
	bool hasSackItem(shared_ptr<S> sack_item);
	shared_ptr<list<shared_ptr<S>>> _getItemsSortedByLossValue();
	virtual void init();
protected:
	int capacity;
	shared_ptr<BreakPartialSolution> break_partial_solution;
	shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_item_list;
	shared_ptr<unordered_map<shared_ptr<S>, shared_ptr<int>>> sack_item_to_count_dict;
	bool ran_init;
	SackProblem(shared_ptr<list<shared_ptr<S>>> loss_sorted_sack_items, int capacity,
		shared_ptr<BreakPartialSolution> break_partial_solution);
	virtual ~SackProblem();
};

// #include "SackProblem.hpp"

class SackSubproblem : public SackProblem {
public:
	shared_ptr<SackProblem> getSourceProblem();
	SackSubproblem(shared_ptr<SackProblem> source_problem, shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			int capacity, shared_ptr<BreakPartialSolution> break_partial_solution);
	virtual ~SackSubproblem() override;
protected:
	weak_ptr<SackProblem> source_problem;
};

// #include "SackProblem.hpp"

// #include "SackSubproblem.hpp"

class NonCoreSackSubproblem : public SackSubproblem {
public:
	shared_ptr<SackItem> getItemWithLowestLossValue();
	shared_ptr<PartialSolution> solve();
	shared_ptr<string> toString();
	NonCoreSackSubproblem(shared_ptr<SackProblem> source_problem, shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			int capacity, shared_ptr<BreakPartialSolution> break_partial_solution);
	virtual ~NonCoreSackSubproblem() override;

};

#include <list>

#include <tuple>

#include <algorithm>

#include <memory>

/*

#include "NonCoreSackSubproblem.hpp"

#include "PostListDecomposeSubproblem.hpp"

#include "SackSubproblem.hpp"

#include "OriginalSackProblem.hpp"

#include "../ListDecomposition.hpp"

*/

using namespace std;

class IntegralityGapEstimate;

class CoreSackSubproblem : public SackSubproblem {
using P_p = PostListDecomposeSubproblem;
using P = PartialSolution;
public:
	shared_ptr<P_p> getLeftPostListDecomposeSubproblem();
	shared_ptr<P_p> getRightPostListDecomposeSubproblem();
	void setLeftPostListDecomposeSubproblem(shared_ptr<P_p> problem);
	void setRightPostListDecomposeSubproblem(shared_ptr<P_p> problem);
	shared_ptr<list<shared_ptr<SackItem>>> getAssumeIncludedBreakPartialSolutionSackItems(shared_ptr<P_p> problem);
	shared_ptr<list<shared_ptr<SackItem>>> getAssumeNotIncludedBreakPartialSolutionSackItems(shared_ptr<P_p> problem);
	shared_ptr<P_p> _getLeftPostListDecomposeSubproblem();
	shared_ptr<P_p> _getRightPostListDecomposeSubproblem();
	shared_ptr<tuple<shared_ptr<P_p>, shared_ptr<P_p>>> divideIntoLeftAndRight();
	shared_ptr<P> getPostListDecomposeSubproblemStarterPartialSolution(shared_ptr<P_p> problem,
			bool is_left_portion);
	shared_ptr<P> combineSolutionsForLeftAndRight(shared_ptr<list<shared_ptr<P>>> left_partial_solutions,
			shared_ptr<list<shared_ptr<P>>> right_partial_solutions);
	shared_ptr<P> combineSolutionsForLeftAndRightBruteForce(shared_ptr<list<shared_ptr<P>>> left_partial_solutions,
			shared_ptr<list<shared_ptr<P>>> right_partial_solutions);
	shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> iterateSolve(shared_ptr<IntegralityGapEstimate> integrality_gap_estimate,
			longlong non_core_subproblem_partial_solution_profit,
			int work_done_by_right, shared_ptr<NonCoreSackSubproblem> non_core_subproblem);
	shared_ptr<P> solve(shared_ptr<IntegralityGapEstimate> integrality_gap_estimate,
			longlong non_core_subproblem_partial_solution_profit);
	shared_ptr<string> toString();
	CoreSackSubproblem(shared_ptr<SackProblem> source_problem, shared_ptr<list<shared_ptr<SackItem>>> sack_items,
			int capacity, shared_ptr<BreakPartialSolution> break_partial_solution);
	virtual ~CoreSackSubproblem() override;
protected:
	shared_ptr<P_p> left_post_list_decompose_subproblem;
	shared_ptr<P_p> right_post_list_decompose_subproblem;

};

// #include "SackSubproblem.hpp"

// #include "../dictionary/Dictionary.hpp"

// #include "../knapsack/PartialSolutionPathLabel.hpp"

// #include "../knapsack/IntegralityGapEstimate.hpp"

// #include "../knapsack/PartialSolution.hpp"

// #include "../knapsack/IdentifierOrderedSackItemTree.hpp"

// #include "CoreSackSubproblem.hpp"

class NonCoreSackSubproblem;

class IntegralityGapEstimate;

class PostListDecomposeSubproblem : public SackSubproblem {
public:
	using P = PartialSolution;
	// using L = list<PartialSolution>;
	using NC = NonCoreSackSubproblem;
	using G = IntegralityGapEstimate;
	static int weightComp(shared_ptr<P> x, shared_ptr<P> y);
	static shared_ptr<list<shared_ptr<P>>>
		mergeOnBasisOfWeight(shared_ptr<list<shared_ptr<P>>> partial_solutions1,
			shared_ptr<list<shared_ptr<P>>> partial_solutions2);
	static shared_ptr<list<shared_ptr<P>>>
		mergeOnBasisOfWeightHelper(shared_ptr<list<shared_ptr<P>>> partial_solutions1,
			shared_ptr<list<shared_ptr<P>>> partial_solutions2,
			shared_ptr<list<shared_ptr<P>>> merged_partial_solutions);
	static shared_ptr<list<shared_ptr<P>>>
		filterOnBasisOfDominateRelation(shared_ptr<list<shared_ptr<P>>> L_curr,
			shared_ptr<NC>(non_core_subproblem));
	static shared_ptr<list<shared_ptr<P>>>
		filterOnBasisOfLossValue(shared_ptr<list<shared_ptr<P>>> L_curr,
			shared_ptr<G> integrality_gap_estimate, shared_ptr<SackItem> sack_item,
			shared_ptr<SackItem> split_sack_item);
	void _setCurrentWinnowedParetoPointsUsingStarterPartialSolution();
	shared_ptr<list<shared_ptr<P>>> _getCurrentWinnowedParetoPoints();
	void _setCurrentWinnowedParetoPoints(shared_ptr<list<shared_ptr<P>>> L_curr);
	void iterateSolve(shared_ptr<SackItem> curr_sack_item,
		shared_ptr<G> integrality_gap_estimate, shared_ptr<NC> non_core_subproblem);
	bool getIsLeftPortion();
	void addItemBasedOnIsStarterItemAndLossValue(shared_ptr<SackItem> sack_item);
	shared_ptr<SackItem> getNextRemainingItemBasedOnIsStarterItemAndLossValue();
	void removeNextRemainingItemBasedOnIsStarterItemAndLossValue();
	bool isFinished();
	// call after constructing
	void init() override;
	PostListDecomposeSubproblem(shared_ptr<SackProblem> source_problem,
			shared_ptr<list<shared_ptr<SackItem>>> sack_items, int capacity,
			shared_ptr<BreakPartialSolution> break_partial_solution,
			bool is_left_portion);
	virtual ~PostListDecomposeSubproblem() override;
protected:
	shared_ptr<list<shared_ptr<SackItem>>> remaining_break_sack_items;
	shared_ptr<list<shared_ptr<SackItem>>> remaining_non_break_sack_items;
	shared_ptr<list<shared_ptr<PartialSolution>>> L_curr;
	bool is_left_portion;
};

#include <list>

#include <tuple>
// #include "SackProblem.hpp"

// #include "CoreSackSubproblem.hpp"

// #include "../knapsack/PartialSolution.hpp"

// #include "../knapsack/IdentifierOrderedSackItemTree.hpp"

class CoreSackSubproblem;

using namespace std;

class OriginalSackProblem : public SackProblem {
	using C = CoreSackSubproblem;
	using D = NonCoreSackSubproblem;
	using G = IntegralityGapEstimate;
public:
	static void moveItemFromNonCoreToCore(shared_ptr<C> core_subproblem, shared_ptr<D> non_core_subproblem,
		shared_ptr<BreakPartialSolution> break_partial_solution, shared_ptr<SackItem> split_sack_item);
	static void ponder(int n);
	shared_ptr<C> getCoreSubproblem();
	shared_ptr<D> getNonCoreSubproblem();
	void setCoreSubproblem(shared_ptr<C> core_subproblem);
	void setNonCoreSubproblem(shared_ptr<D> non_core_subproblem);
	shared_ptr<list<shared_ptr<SackItem>>> _getCoreSackItems(longdouble cutoff_loss_value);
	shared_ptr<list<shared_ptr<SackItem>>> _getNonCoreSackItems(longdouble cutoff_loss_value);
	shared_ptr<list<shared_ptr<SackItem>>> _getNonCoreIncludedItems(longdouble cutoff_loss_value);
	int _getNonCoreIncludedItemTotalWeight(longdouble cutoff_loss_value);
	shared_ptr<C> _getCoreSubproblem(longdouble cutoff_loss_value);
	shared_ptr<D> _getNonCoreSubproblem(longdouble cutoff_loss_value);
	shared_ptr<tuple<shared_ptr<C>, shared_ptr<D>>> divideIntoCoreAndNonCore(longdouble cutoff_loss_value);
	bool canStopExpandingCoreSubproblem(shared_ptr<C> core_subproblem,
			shared_ptr<D> non_core_subproblem, shared_ptr<G> integrality_gap_estimate);
	shared_ptr<list<shared_ptr<SackItem>>> solve();
	OriginalSackProblem(shared_ptr<list<shared_ptr<SackItem>>> sack_items, int capacity,
			shared_ptr<BreakPartialSolution> break_partial_solution);
	virtual ~OriginalSackProblem() override;
protected:
	shared_ptr<C> core_subproblem;
	shared_ptr<D> non_core_subproblem;

};

#endif

#ifndef FEED_OPTIMIZER_SOLUTION_HPP
#define FEED_OPTIMIZER_SOLUTION_HPP

#endif

#ifndef KNAPSACK_IDENTIFIER_ORDERED_SACK_ITEM_TREE_T_HPP
#define KNAPSACK_IDENTIFIER_ORDERED_SACK_ITEM_TREE_T_HPP

#include <memory>

// #include "IdentifierOrderedSackItemTree.hpp"

// #include "Solution.hpp"

/*

using E4 = STEntry<SackItem, SackItem, int>;

using N5 = STNode<SackItem, SackItem, int>;

using U = IdentifierOrderedSackItemTree;

template <>
inline shared_ptr<int> BinarySearchTree<SackItem, SackItem, int>::
	_key_transform(shared_ptr<SackItem> x) {
	return make_shared<int>(*(new int(x->getIDValue())));
}

template <>
inline int BinarySearchTree<SackItem, SackItem, int>::
	_comparator(shared_ptr<int> a, shared_ptr<int> b) {
	if (*a == *b) {
		return 0;
	} else if (*a > *b) {
		return 1;
	} else {
		// a < b
		return -1;
	}
}

*/

/*

template <>
inline shared_ptr<string> BSTEntry<SackItem, SackItem, int>::toString() {

shared_ptr<string> key_str = this->key->toString();
shared_ptr<string> value_str = this->value->toString();
shared_ptr<string> output_str = make_shared<string>(*(new string("(" + *key_str + ", " + *value_str + ")")));
// shared_ptr<string> output_str_shared_ptr = make_shared<string>(*output_str);
// return output_str_shared_ptr;
return output_str;
}

*/

/*

template <>
inline shared_ptr<string> BSTEntry<SackItem, SackItem, int>::toKeyString() {
	shared_ptr<string> key_str = this->key->toString();
	// shared_ptr<string> output_str_shared_ptr = make_shared<string>(*key_str);
	// return output_str_shared_ptr;
	return key_str;
}

*/

#endif

#ifndef DICTIONARY_DICTIONARY_T_HPP
#define DICTIONARY_DICTIONARY_T_HPP

// #include "Solution.hpp"

// #include "../knapsack/SackItem.hpp"

// #include "../knapsack/PartialSolution.hpp"

// #include "../knapsack/IdentifierOrderedSackItemTree.hpp"

// #include "Solution.hpp"

// #include "../feed_optimizer/FeedItem.hpp"

// #include "FeedProblem.hpp"

template <typename A, typename B>
using M = unordered_multimap<shared_ptr<A>, shared_ptr<B>, function<size_t(const shared_ptr<A> a)>,
		function<bool(const shared_ptr<A> a, const shared_ptr<A> b)>>;

shared_ptr<string> getKVPairString(shared_ptr<list<shared_ptr<tuple<shared_ptr<int>,
		shared_ptr<int>>>>> tuple_list);

template <typename A, typename B>
void Dictionary<A, B>::ponder(int n) {

	// cout << "hello" << endl;

	shared_ptr<Dictionary<int, int>> d =
			shared_ptr<Dictionary<int, int>>(new Dictionary<int, int>());
	d->insert(shared_ptr<int>(new int(1)), shared_ptr<int>(new int(1)));
	d->insert(shared_ptr<int>(new int(1)), shared_ptr<int>(new int(2)));
	shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> result =
			d->find(shared_ptr<int>(new int(1)));
	cout << "result 1" << endl;
	cout << to_string(*(get<0>(*result))) << " " << to_string(*(get<1>(*result))) << endl;
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> matches =
			d->findAll(shared_ptr<int>(new int(1)));
	d->insert(shared_ptr<int>(new int(2)), shared_ptr<int>(new int(1)));
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> result2 =
			d->findAll(shared_ptr<int>(new int(2)));
	shared_ptr<string> result_str2 = getKVPairString(result2);
	cout << "result 2" << endl;
	cout << *result_str2;
	d->insert(shared_ptr<int>(new int(3)), shared_ptr<int>(new int(1)));
	d->insert(shared_ptr<int>(new int(3)), shared_ptr<int>(new int(1)));
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> result3 =
			d->findAll(shared_ptr<int>(new int(3)));
	shared_ptr<string> result_str3 = getKVPairString(result3);
	cout << "result 3" << endl;
	cout << *result_str3;
	d->insert(shared_ptr<int>(new int(4)), shared_ptr<int>(new int(1)));
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> result4 =
			d->findAll(shared_ptr<int>(new int(4)));
	shared_ptr<string> result_str4 = getKVPairString(result4);
	cout << "result 4" << endl;
	cout << *result_str4;
	// paradoxical effect; remove on basis of key only
	d->remove(shared_ptr<tuple<shared_ptr<int>,
			shared_ptr<int>>>(new tuple<shared_ptr<int>,
					shared_ptr<int>>(shared_ptr<int>(new int(3)),
							shared_ptr<int>(new int(1)))));
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> result5 =
			d->findAll(shared_ptr<int>(new int(3)));
	shared_ptr<string> result_str5 = getKVPairString(result5);
	cout << "result 5" << endl;
	cout << *result_str5;
	d->remove(shared_ptr<tuple<shared_ptr<int>,
			shared_ptr<int>>>(new tuple<shared_ptr<int>,
					shared_ptr<int>>(shared_ptr<int>(new int(4)),
							shared_ptr<int>(new int(1)))));
	int size = d->getSize();
	cout << "result 6" << endl;
	cout << to_string(size) << endl;
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> entries = d->entries();
	cout << "result 7" << endl;
	cout << *(getKVPairString(entries));
	cout << "result 8" << endl;
	cout << *(d->toString());
}

template <typename A, typename B>
int Dictionary<A, B>::getSize() {
	return this->size;
}

template <typename A, typename B>
bool Dictionary<A, B>::isEmpty() {
	return this->getSize() == 0;
}

template <typename A, typename B>
shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> Dictionary<A, B>::find(shared_ptr<A> k) {

	// if value for given key does not exist, return null pointer

	// otherwise, choose an arbitrary value
	// in associated list of values and package
	// as an entry (a key-value pair)

	// cout << "finding a pair for a particular key" << endl;

	shared_ptr<M> map = this->_getEntryMap();
	if (map->count(k) == 0) {
		return NULL;
	} else {
		auto iterator = map->find(k);
		pair<shared_ptr<A>, shared_ptr<B>> curr_pair = *iterator;
		shared_ptr<int> curr_key = curr_pair.first;
		shared_ptr<int> curr_value = curr_pair.second;
		shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> curr_tuple =
				shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>(new
						tuple<shared_ptr<A>, shared_ptr<B>>(curr_key, curr_value));
		return curr_tuple;
	}
}

template <typename A, typename B>
shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> Dictionary<A, B>::findAll(shared_ptr<A> k) {

	// cout << "finding all pairs for a particular key" << endl;

	shared_ptr<M> map = this->_getEntryMap();
	if (map->count(k) == 0) {
		return NULL;
	} else {
	auto range = map->equal_range(k);
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> entries =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>>(new
					list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>());
	auto range_begin = range.first;
	auto range_end = range.second;
	auto iterator = range_begin;
	while (iterator != range_end) {
		pair<shared_ptr<A>, shared_ptr<B>> curr_pair = *iterator;
		// relying on idea that curr_key and curr_value will survive
		shared_ptr<A> curr_key = curr_pair.first;
		shared_ptr<B> curr_value = curr_pair.second;
		shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> curr_tuple =
				shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>(new
						tuple<shared_ptr<A>, shared_ptr<B>>(curr_key, curr_value));
		entries->push_back(curr_tuple);
		advance(iterator, 1);
	}
	return entries;
	}
}

template <typename A, typename B>
void Dictionary<A, B>::insert(shared_ptr<A> k, shared_ptr<B> v) {

	// cout << "inserting a key-value pair" << endl;

	shared_ptr<M> map = this->_getEntryMap();
	pair<shared_ptr<A>, shared_ptr<B>> curr_pair =
			pair<shared_ptr<A>, shared_ptr<B>>(*(new
					pair<shared_ptr<A>, shared_ptr<B>>(k, v)));
	map->insert(curr_pair);
	this->size = this->size + 1;
}

// remove on basis of key

template <typename A, typename B>
void Dictionary<A, B>::remove(shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> e) {

	// cout << "removing a key-value pair" << endl;

	shared_ptr<M> map = this->_getEntryMap();
	shared_ptr<A> k = get<0>(*e);
	shared_ptr<B> v = get<1>(*e);
	pair<shared_ptr<A>, shared_ptr<B>> curr_pair = *(new pair<shared_ptr<A>, shared_ptr<B>>(k, v));
	auto iterator = map->find(k);
	map->erase(iterator);
	this->size = this->size - 1;
}

template <typename A, typename B>
shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> Dictionary<A, B>::entries() {

	// cout << "retrieving entries" << endl;

	// retrieve all key-value pairs

	shared_ptr<M> map = this->_getEntryMap();
	auto iterator = map->begin();
	shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>> entries =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>>(new
					list<shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>>());
	while (iterator != map->end()) {
		pair<shared_ptr<A>, shared_ptr<B>> curr_pair = *iterator;
		shared_ptr<A> curr_key = curr_pair.first;
		shared_ptr<B> curr_value = curr_pair.second;
		tuple<shared_ptr<A>, shared_ptr<B>> *curr_tuple =
				new tuple<shared_ptr<A>, shared_ptr<B>>(curr_key, curr_value);
		shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>> curr_tuple_shared_ptr =
				shared_ptr<tuple<shared_ptr<A>, shared_ptr<B>>>(curr_tuple);
		entries->push_back(curr_tuple_shared_ptr);
		advance(iterator, 1);
	}
	return entries;
}

template <typename A, typename B>
shared_ptr<M<A, B>> Dictionary<A, B>::_getEntryMap() {
	return this->entry_map;
}

template <typename A, typename B>
shared_ptr<string> Dictionary<A, B>::toString() {
	throw "not implemented";
}

template <>
inline shared_ptr<string> Dictionary<int, int>::toString() {
	// cout << "retrieving a string version of a dictionary" << endl;
	shared_ptr<M> map = this->_getEntryMap();
	auto iterator = map->begin();
	string result_str = "";
	while (iterator != map->end()) {
		pair<shared_ptr<int>, shared_ptr<int>> curr_pair = *iterator;
		shared_ptr<int> key = curr_pair.first;
		shared_ptr<int> value = curr_pair.second;
		string curr_result_str = "(" + to_string(*key) + ", " + to_string(*value) + ")";
		result_str = result_str + curr_result_str + " ";
		advance(iterator, 1);
	}
	shared_ptr<string> result = shared_ptr<string>(new string(result_str));
	return result;
}

template <>
inline shared_ptr<string> Dictionary<int, SackItem>::toString() {
	shared_ptr<M> map = this->_getEntryMap();
	auto iterator = map->begin();
	string result_str = "";
	while(iterator != map->end()) {
		pair<shared_ptr<int>, shared_ptr<SackItem>> curr_pair = *iterator;
		shared_ptr<int> key = curr_pair.first;
		shared_ptr<SackItem> value = curr_pair.second;
		string curr_result_str = "(" + to_string(*key) + ", " + *(value->toString()) + ")";
		result_str = result_str + curr_result_str + " ";
		advance(iterator, 1);
	}
	shared_ptr<string> result = shared_ptr<string>(new string(result_str));
	return result;
}

template <>
inline shared_ptr<string> Dictionary<int, FeedItem>::toString() {
	shared_ptr<M> map = this->_getEntryMap();
	auto iterator = map->begin();
	string result_str = "";
	while(iterator != map->end()) {
		pair<shared_ptr<int>, shared_ptr<FeedItem>> curr_pair = *iterator;
		shared_ptr<int> key = curr_pair.first;
		shared_ptr<FeedItem> value = curr_pair.second;
		string curr_result_str = "(" + to_string(*key) + ", " + *(value->toString()) + ")";
		result_str = result_str + curr_result_str + " ";
		advance(iterator, 1);
	}
	shared_ptr<string> result = shared_ptr<string>(new string(result_str));
	return result;
}

template <typename A, typename B>
Dictionary<A, B>::Dictionary() {
	this->entry_map = shared_ptr<M>(new M(5, hash_fn<A>, key_equal_fn<A>));
	this->size = 0;
}

template <typename A, typename B>
Dictionary<A, B>::~Dictionary() {
	// cout << "destructing a dictionary" << endl;
	(this->entry_map).reset();
}

// #include "DoublyLinkedList.hpp"

// #include "Solution.hpp"

using namespace std;

template <typename E>
using N_l = DoublyLinkedListNode<E>;

template <typename E>
using L = DoublyLinkedList<E>;

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedList<E>::_createNode(shared_ptr<E> item,
		shared_ptr<N_l> prev, shared_ptr<N_l> next) {
	shared_ptr<N_l> node = shared_ptr<N_l>(new DoublyLinkedListNode<E>(item, prev, next));
	return node;
}

template <typename E>
void DoublyLinkedList<E>::ponder(int n) {

	shared_ptr<DoublyLinkedList<int>> l =
			shared_ptr<DoublyLinkedList<int>>(new DoublyLinkedList<int>());

	shared_ptr<DoublyLinkedListNode<int>> node1 =
			shared_ptr<DoublyLinkedListNode<int>>(new
					DoublyLinkedListNode<int>(shared_ptr<int>(new int(1)), NULL, NULL));

	shared_ptr<DoublyLinkedListNode<int>> node2 =
			shared_ptr<DoublyLinkedListNode<int>>(new
					DoublyLinkedListNode<int>(shared_ptr<int>(new int(2)), NULL, NULL));

	shared_ptr<DoublyLinkedListNode<int>> node3 =
			shared_ptr<DoublyLinkedListNode<int>>(new
					DoublyLinkedListNode<int>(shared_ptr<int>(new int(3)), NULL, NULL));

	shared_ptr<DoublyLinkedListNode<int>> node4 =
			shared_ptr<DoublyLinkedListNode<int>>(new
					DoublyLinkedListNode<int>(shared_ptr<int>(new int(4)), NULL, NULL));

l->addFirst(node1);

l->addLast(node4);

l->addBefore(node3, node4);

l->addAfter(node2, node1);

l->remove(node1);

shared_ptr<list<shared_ptr<int>>> element_list = l->toElementList();

shared_ptr<list<shared_ptr<DoublyLinkedListNode<int>>>> node_list = l->_toNodeList();

shared_ptr<list<shared_ptr<string>>> element_str_list =
		shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());

element_str_list->resize(element_list->size(), NULL);

transform(element_list->begin(), element_list->end(),
		element_str_list->begin(),
		[&] (shared_ptr<int> a)
		{ return shared_ptr<string>(new string(to_string(*a))); });

shared_ptr<list<shared_ptr<string>>> node_str_list =
		shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());

node_str_list->resize(node_list->size(), NULL);

transform(node_list->begin(), node_list->end(),
		node_str_list->begin(),
		[&] (shared_ptr<DoublyLinkedListNode<int>> a)
		{ shared_ptr<int> element = a->getElement();
		return shared_ptr<string>(new string(to_string(*element))); });

shared_ptr<string> element_str_list_str = accumulate(element_str_list->begin(),
		element_str_list->end(), shared_ptr<string>(new string("")),
		[&] (shared_ptr<string> a, shared_ptr<string> b)
		{ return shared_ptr<string>(new string(*a + *b)); });

shared_ptr<string> node_str_list_str = accumulate(node_str_list->begin(),
		node_str_list->end(), shared_ptr<string>(new string("")),
		[&] (shared_ptr<string> a, shared_ptr<string> b)
		{ return shared_ptr<string>(new string(*a + *b)); });

cout << *element_str_list_str << endl;

cout << *node_str_list_str << endl;

}

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedList<E>::_getHeaderSentinel() {
	return this->header;
}

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedList<E>::_getTrailerSentinel() {
	return this->trailer;
}

template <typename E>
int DoublyLinkedList<E>::getSize() {
	return this->size;
}

template <typename E>
bool DoublyLinkedList<E>::isEmpty() {
	return this->getSize() == 0;
}

template <typename E>
void DoublyLinkedList<E>::addBefore(shared_ptr<N_l> v, shared_ptr<N_l> z) {
	shared_ptr<N_l> w = z->getPrev();
	v->setPrev(w);
	v->setNext(z);
	w->setNext(v);
	z->setPrev(v);
	this->size = this->size + 1;
}

template <typename E>
void DoublyLinkedList<E>::addAfter(shared_ptr<N_l> v, shared_ptr<N_l> z) {
	shared_ptr<N_l> w = z->getNext();
	v->setPrev(z);
	v->setNext(w);
	w->setPrev(v);
	z->setNext(v);
	this->size = this->size + 1;
}

template <typename E>
void DoublyLinkedList<E>::remove(shared_ptr<N_l> v) {
	shared_ptr<N_l> u = v->getPrev();
	shared_ptr<N_l> w = v->getNext();
	w->setPrev(u);
	u->setNext(w);
	v->setPrev(NULL);
	v->setNext(NULL);
	this->size = this->size - 1;
}

template <typename E>
void DoublyLinkedList<E>::addFirst(shared_ptr<N_l> v) {
	this->addAfter(v, this->header);
}

template <typename E>
void DoublyLinkedList<E>::addLast(shared_ptr<N_l> v) {
	this->addBefore(v, this->trailer);
}

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedList<E>::getFirst() {
	return this->header->getNext();
}

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedList<E>::getLast() {
	return this->trailer->getPrev();
}

template <typename E>
bool DoublyLinkedList<E>::hasPredecessor(shared_ptr<N_l> node) {
	shared_ptr<N_l> predecessor = node->getPrev();
	bool has_predecessor = predecessor != NULL
			&& predecessor != this->_getHeaderSentinel();
	return has_predecessor;
}

template <typename E>
bool DoublyLinkedList<E>::hasSuccessor(shared_ptr<N_l> node) {
	shared_ptr<N_l> successor = node->getNext();
	bool has_successor = successor != NULL
			&& successor != this->_getTrailerSentinel();
	return has_successor;
}

template <typename E>
shared_ptr<list<shared_ptr<E>>> DoublyLinkedList<E>::toElementList() {
	shared_ptr<list<shared_ptr<E>>> elements =
			shared_ptr<list<shared_ptr<E>>>(this->
					_toElementListHelper(this->_getHeaderSentinel(),
							shared_ptr<list<shared_ptr<E>>>(new list<shared_ptr<E>>())));
	return elements;
}

template <typename E>
shared_ptr<list<shared_ptr<E>>> DoublyLinkedList<E>::_toElementListHelper(shared_ptr<N_l> node,
		shared_ptr<list<shared_ptr<E>>> partial_element_list) {
	if (this->_getTrailerSentinel() == node) {
		return partial_element_list;
	} else if (this->_getHeaderSentinel() == node) {
		return this->_toElementListHelper(node->getNext(), partial_element_list);
	} else {
		shared_ptr<E> curr_element = node->getElement();
		shared_ptr<list<shared_ptr<E>>> additions =
				shared_ptr<list<shared_ptr<E>>>(new list<shared_ptr<E>>());
		additions->push_back(curr_element);
		shared_ptr<list<shared_ptr<E>>> next_partial_element_list =
				shared_ptr<list<shared_ptr<E>>>(new list<shared_ptr<E>>());
		next_partial_element_list->splice(next_partial_element_list->end(),
				*partial_element_list, partial_element_list->begin(),
				partial_element_list->end());
		next_partial_element_list->splice(next_partial_element_list->end(),
				*additions, additions->begin(), additions->end());
		return this->_toElementListHelper(node->getNext(),
				next_partial_element_list);
	}
}

template <typename E>
shared_ptr<list<shared_ptr<N_l<E>>>> DoublyLinkedList<E>::_toNodeList() {
	shared_ptr<list<shared_ptr<N_l>>> nodes =
			this->_toNodeListHelper(this->_getHeaderSentinel(),
					shared_ptr<list<shared_ptr<N_l>>>(new
							list<shared_ptr<N_l>>()));
	return nodes;
}

template <typename E>
shared_ptr<list<shared_ptr<N_l<E>>>> DoublyLinkedList<E>::_toNodeListHelper(shared_ptr<N_l> node,
		shared_ptr<list<shared_ptr<N_l>>> partial_node_list) {
	if (this->_getTrailerSentinel() == node) {
		return partial_node_list;
	} else if (this->_getHeaderSentinel() == node) {
		return this->_toNodeListHelper(node->getNext(), partial_node_list);
	} else {
		shared_ptr<N_l> curr_node = node;
		shared_ptr<list<shared_ptr<N_l>>> additions =
				shared_ptr<list<shared_ptr<N_l>>>(new list<shared_ptr<N_l>>());
		additions->push_back(curr_node);
		shared_ptr<list<shared_ptr<N_l>>> next_partial_node_list =
				shared_ptr<list<shared_ptr<N_l>>>(new list<shared_ptr<N_l>>());
		next_partial_node_list->splice(next_partial_node_list->end(),
				*partial_node_list, partial_node_list->begin(),
				partial_node_list->end());
		next_partial_node_list->splice(next_partial_node_list->end(),
				*additions, additions->begin(), additions->end());
		return this->_toNodeListHelper(node->getNext(), next_partial_node_list);
	}
}

template <typename E>
shared_ptr<string> DoublyLinkedList<E>::toString() {
	shared_ptr<list<shared_ptr<N_l>>> node_list =
			this->_toNodeList();
	shared_ptr<list<shared_ptr<E>>> element_list =
			shared_ptr<list<shared_ptr<E>>>(new list<shared_ptr<E>>());
	element_list->resize(node_list->size(), NULL);
	transform(node_list->begin(), node_list->end(), element_list->begin(),
			[&] (shared_ptr<N_l> a) { return a->getElement(); });
	shared_ptr<list<shared_ptr<string>>> element_str_list =
			shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());
	transform(element_list->begin(), element_list->end(), element_str_list->begin(),
			[&] (shared_ptr<E> a) { return a->toString(); });
	shared_ptr<string> partial_result_str = NULL;
	if (element_str_list->size() == 0) {
		partial_result_str = shared_ptr<string>(new string(""));
	} else {
		partial_result_str = accumulate(element_str_list->begin(),
				element_str_list->end(), "",
				[&] (shared_ptr<string> a, shared_ptr<string> b)
				{ return shared_ptr<string>(new string(*a + ", " + *b)); });
	}
	shared_ptr<string> result_str =
			shared_ptr<string>(new string("List(" + *partial_result_str + ")"));
	return result_str;
}

template <typename E>
DoublyLinkedList<E>::DoublyLinkedList() {
	this->header = DoublyLinkedList<E>::_createNode(NULL, NULL, NULL);
	this->trailer = DoublyLinkedList<E>::_createNode(NULL, this->header, NULL);
	(this->header)->setNext(this->trailer);
	this->size = 0;
}

template <typename E>
DoublyLinkedList<E>::~DoublyLinkedList() {
	(this->header).reset();
	(this->trailer).reset();
}

// #include "DoublyLinkedListNode.hpp"

template <typename E>
using N_l = DoublyLinkedListNode<E>;

template <typename E>
using L = DoublyLinkedList<E>;

template <typename E>
shared_ptr<E> DoublyLinkedListNode<E>::getElement() {
	return this->element;
}

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedListNode<E>::getPrev() {
	return this->prev;
}

template <typename E>
shared_ptr<N_l<E>> DoublyLinkedListNode<E>::getNext() {
	return this->next;
}

template <typename E>
void DoublyLinkedListNode<E>::setElement(shared_ptr<E> element) {
	this->element = element;
}

template <typename E>
void DoublyLinkedListNode<E>::setPrev(shared_ptr<N_l> prev) {
	this->prev = prev;
}

template <typename E>
void DoublyLinkedListNode<E>::setNext(shared_ptr<N_l> next) {
	this->next = next;
}

template <typename E>
DoublyLinkedListNode<E>::DoublyLinkedListNode(shared_ptr<E> element,
		shared_ptr<N_l> prev, shared_ptr<N_l> next) {
	this->element = element;
	this->prev = prev;
	this->next = next;
}

template <typename E>
DoublyLinkedListNode<E>::~DoublyLinkedListNode() {
	cout << "destructing a doubly-linked-list node" << endl;
	(this->element).reset();
	(this->prev).reset();
	(this->next).reset();
}

#endif

// #include "IdentifierOrderedSackItemTree.t.hpp"

// #include "Solution.t.hpp"

using U = IdentifierOrderedSackItemTree;

bool compare(const int a, const int b) {
	return a < b;
}

shared_ptr<IdentifierOrderedSackItemTree>
	IdentifierOrderedSackItemTree::
		construct(shared_ptr<list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>> entries) {
	shared_ptr<U> tree = shared_ptr<U>(new IdentifierOrderedSackItemTree());
	// tree->init();
	for (shared_ptr<tuple<int, shared_ptr<SackItem>>> curr_entry : *entries) {
		int key;
		shared_ptr<SackItem> value;
		tie(key, value) = *curr_entry;
		// tree->insert(key, value);
		(tree->id_value_to_sack_item_map)->insert(pair<int,
				shared_ptr<SackItem>>(key, value));
	}
	return tree;
}

void IdentifierOrderedSackItemTree::ponder(int n) {
	shared_ptr<list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>> entries =
			shared_ptr<list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>>(new
					list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>());
	shared_ptr<U> t4 = IdentifierOrderedSackItemTree::construct(entries);
	shared_ptr<SackItem> sack_item1 = shared_ptr<SackItem>(new SackItem(3, 5, 3));
	shared_ptr<SackItem> sack_item2 = shared_ptr<SackItem>(new SackItem(2, 1, 6));
	shared_ptr<SackItem> sack_item3 = shared_ptr<SackItem>(new SackItem(3, 2, 8));
	t4->insertSackItem(sack_item1);
	t4->insertSackItem(sack_item2);
	t4->insertSackItem(sack_item3);
	// cout << "pre-remove: " + *(t4->toString()) << endl;
	t4->removeSackItem(sack_item2->getIDValue());
	// cout << "post-remove: " + *(t4->toString()) << endl;
}

/*
template <typename K, typename V, typename L>
using R = BSTEntry<K, V, L>;

template <typename K, typename V, typename L>
using N1 = BSTNode<K, V, L>;
*/

// returns a tuple result given a sack item

shared_ptr<SackItem>
	IdentifierOrderedSackItemTree::findSackItem(int id_value) {
	int key = id_value;
	auto result = (this->id_value_to_sack_item_map)->find(key);
	if (result == (this->id_value_to_sack_item_map)->end()) {
		return NULL;
	} else {
		pair<int, shared_ptr<SackItem>> result_pair = *result;
		shared_ptr<SackItem> found_sack_item = result_pair.second;
		return found_sack_item;
	}
}

shared_ptr<SackItem> IdentifierOrderedSackItemTree::
	insertSackItem(shared_ptr<SackItem> sack_item) {
	int untransformed_key = sack_item->getIDValue();
	shared_ptr<SackItem> value = sack_item;
	(this->id_value_to_sack_item_map)->insert(pair<int,
			shared_ptr<SackItem>>(untransformed_key, value));
	shared_ptr<SackItem> result = sack_item;
	return result;
}

void IdentifierOrderedSackItemTree::removeSackItem(int id_value) {
	int key = id_value;
	auto iterator = (this->id_value_to_sack_item_map)->find(key);
	(this->id_value_to_sack_item_map)->erase(iterator);
}

shared_ptr<list<shared_ptr<SackItem>>> IdentifierOrderedSackItemTree::toIdentifierOrderedSackItemList() {
	auto start_iterator = (this->id_value_to_sack_item_map)->begin();
	auto end_iterator = (this->id_value_to_sack_item_map)->end();
	int num_items = (this->id_value_to_sack_item_map)->size();
	shared_ptr<list<shared_ptr<SackItem>>> identifier_ordered_sack_item_list =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	for_each(start_iterator, end_iterator, [&] (pair<int, shared_ptr<SackItem>> a)
			{ identifier_ordered_sack_item_list->push_back(a.second); });
	return identifier_ordered_sack_item_list;
}

shared_ptr<U> IdentifierOrderedSackItemTree::clone() {
	/*
	shared_ptr<T2> tree = this->deepCloneWithClonedEntries();
	shared_ptr<U> next_tree = static_pointer_cast<U>(tree);
	return next_tree;
	*/
	shared_ptr<U> tree = shared_ptr<U>(new IdentifierOrderedSackItemTree());
	// be careful not to create two shared pointers using same raw pointer
	// tree->id_value_to_sack_item_map = make_shared<Y>(*(this->id_value_to_sack_item_map));
	shared_ptr<Y> next_map = shared_ptr<Y>(new Y(*(this->id_value_to_sack_item_map)));
	tree->id_value_to_sack_item_map = next_map;
	return tree;
}

/*

shared_ptr<BinaryTree<BSTEntry<SackItem, SackItem, int>>> IdentifierOrderedSackItemTree::_createTree() {
	shared_ptr<list<shared_ptr<tuple<shared_ptr<SackItem>, shared_ptr<SackItem>>>>> entry_list =
			make_shared<list<shared_ptr<tuple<shared_ptr<SackItem>, shared_ptr<SackItem>>>>>(*(new
					list<shared_ptr<tuple<shared_ptr<SackItem>, shared_ptr<SackItem>>>>));
	shared_ptr<U> tree = U::construct(entry_list);
	return tree;
}

*/

/*

void IdentifierOrderedSackItemTree::init() {
	SplayTree<SackItem, SackItem, int>::init();
}

*/

IdentifierOrderedSackItemTree::IdentifierOrderedSackItemTree() {
	this->id_value_to_sack_item_map = shared_ptr<Y>(new Y(compare));
}

IdentifierOrderedSackItemTree::~IdentifierOrderedSackItemTree() {
	// cout << "destructing an identifier-ordered sack item tree" << endl;
}

// #include "SackItem.hpp"

// #include "PartialSolution.hpp"

using namespace std;

namespace Util {

string intToString(int a) {
	char *str;
	int buffer_size = snprintf((char *) NULL, 0, "%d", a) + 1;
	str = (char *) malloc(sizeof(char) * buffer_size);
	snprintf((char *) str, buffer_size, "%d", a);
	// free(str);
	string result = (string) str;
	free(str);
	return result;
}

string longdoubleToString(longdouble a) {
	char *str;
	int buffer_size = snprintf((char *) NULL, 0, "%f", a) + 1;
	str = (char *) malloc(sizeof(char) * buffer_size);
	snprintf((char *) str, buffer_size, "%f", a);
	// free(str);
	string result = (string) str;
	free(str);
	return result;
}

string longlongToString(longlong a) {
	char *str;
	int buffer_size = snprintf((char *) NULL, 0, "%ld", a) + 1;
	str = (char *) malloc(sizeof(char) * buffer_size);
	snprintf((char *) str, buffer_size, "%ld", a);
	// free(str);
	string result = (string) str;
	free(str);
	return result;
}

shared_ptr<tuple<shared_ptr<int>, shared_ptr<int>>>
	makeIntSharedPtrTuple(int a, int b) {
	shared_ptr<int> a_ptr = shared_ptr<int>(new int(a));
	shared_ptr<int> b_ptr = shared_ptr<int>(new int(b));
	// shared_ptr<int> a_shared_ptr = make_shared<int>(*a_ptr);
	// shared_ptr<int> b_shared_ptr = make_shared<int>(*b_ptr);
	shared_ptr<tuple<shared_ptr<int>, shared_ptr<int>>> result_tuple =
			shared_ptr<tuple<shared_ptr<int>, shared_ptr<int>>>(new tuple<shared_ptr<int>,
			shared_ptr<int>>(a_ptr, b_ptr));
	return result_tuple;

	/*

	shared_ptr<tuple<shared_ptr<int>, shared_ptr<int>>>
			result_tuple_shared_ptr =
					make_shared<tuple<shared_ptr<int>,
					shared_ptr<int>>>(*result_tuple);
	return result_tuple_shared_ptr;

	*/
}

int comp(longdouble x, longdouble y) {
	if (x < y) {
		return -1;
	} else if (x > y) {
		return 1;
	} else {
		// x == y
		return 0;
	}
}

// consider de-referencing pointers

shared_ptr<list<shared_ptr<int>>>
	removeDuplicateValuesGivenSortedValues(shared_ptr<list<shared_ptr<int>>> values) {
	if (values->size() == 0) {
		return shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	} else {
		shared_ptr<int> value = values->front();
		shared_ptr<list<shared_ptr<int>>> result_values =
				shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
		result_values->push_back(value);
		shared_ptr<list<shared_ptr<int>>> next_values =
				shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>(*values));
		next_values->pop_front();
		shared_ptr<int> prev_value = value;
		shared_ptr<list<shared_ptr<int>>> unique_values =
				shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
		shared_ptr<list<shared_ptr<int>>> other_result_values =
				Util::removeDuplicateValuesGivenSortedValuesHelper(next_values,
						prev_value, unique_values);
		result_values->splice(result_values->end(), *other_result_values);
		return result_values;
	}

}

// list values get cannibalized

shared_ptr<list<shared_ptr<int>>>
	removeDuplicateValuesGivenSortedValuesHelper(shared_ptr<list<shared_ptr<int>>> values,
		shared_ptr<int> prev_value, shared_ptr<list<shared_ptr<int>>> unique_values) {
if (values->size() == 0) {
	return unique_values;
} else {
	shared_ptr<int> curr_value = values->front();
	if (*curr_value == *prev_value) {
		shared_ptr<list<shared_ptr<int>>> next_values = values;
		next_values->pop_front();
		shared_ptr<int> next_prev_value = curr_value;
		shared_ptr<list<shared_ptr<int>>> next_unique_values = unique_values;
		return Util::removeDuplicateValuesGivenSortedValuesHelper(next_values,
				next_prev_value, next_unique_values);
	} else {
		shared_ptr<list<shared_ptr<int>>> next_values = values;
		next_values->pop_front();
		shared_ptr<int> next_prev_value = curr_value;
		shared_ptr<list<shared_ptr<int>>> next_unique_values = unique_values;
		next_unique_values->push_back(curr_value);
		return Util::removeDuplicateValuesGivenSortedValuesHelper(next_values,
				next_prev_value, next_unique_values);
	}
}
}

void ponder(int n) {
	list<int> sorted_values = {1, 2, 3, 4, 5, 6, 6, 7};
	shared_ptr<list<shared_ptr<int>>> next_sorted_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	for_each(sorted_values.begin(), sorted_values.end(),
			[&] (int a)  { next_sorted_values->push_back(shared_ptr<int>(new int(a))); });
	shared_ptr<list<shared_ptr<int>>> result =
			Util::removeDuplicateValuesGivenSortedValues(next_sorted_values);
	for_each(result->begin(), result->end(),
			[&] (shared_ptr<int> a) { cout << *a << " "; });
}

}

// #include "SackItem.hpp"

// #include "../util/Util.hpp"

longlong SackItem::getProfit() {
	return this->profit;
}

int SackItem::getWeight() {
	return this->weight;
}

int SackItem::getIDValue() {
	return this->id_value;
}

void SackItem::setProfit(longlong profit) {
	this->profit = profit;
}

void SackItem::setWeight(int weight) {
	this->weight = weight;
}


void SackItem::setIDValue(int id_value) {
	this->id_value = id_value;
}

longdouble SackItem::getProfitWeightRatio() {
	longdouble profit = (longdouble) this->getProfit();
	longdouble weight = (longdouble) this->getWeight();
	longdouble ratio = profit / weight;
	return ratio;
}

longdouble SackItem::getLossValue(shared_ptr<SackItem> split_sack_item, bool is_included) {

	// cout << "split sack item: " + *(split_sack_item->toString()) << endl;

	longdouble ratio = split_sack_item->getProfitWeightRatio();
	longdouble profit = (longdouble) this->getProfit();
	longdouble weight = (longdouble) this->getWeight();
	longdouble signed_loss_value = profit - (ratio * weight);
	// cout << ratio << " " << profit << " " << weight << endl;
	// cout << "signed loss value: " << to_string(signed_loss_value) << endl;
	longdouble loss_value = abs(signed_loss_value);
	// cout << "non-signed loss value: " << to_string(loss_value) << endl;
	return loss_value;
}

shared_ptr<string> SackItem::toString() {
	longlong profit = this->getProfit();
	int weight = this->getWeight();
	int identifier_value = this->getIDValue();
	/*
	string result = "(" + to_string(profit) + ", " + to_string(weight) +
			", " + to_string(identifier_value) + ")";
	*/
	string result_str = "(" + Util::longlongToString(profit)
			+ ", " + Util::intToString(weight) +
			", " + Util::intToString(identifier_value) + ")";
	shared_ptr<string> result = shared_ptr<string>(new string(result_str));
	return result;
}

SackItem::SackItem(longlong profit, int weight, int id_value) {
	this->profit = profit;
	this->weight = weight;
	this->id_value = id_value;
}

SackItem::~SackItem() {

}

// #include "PartialSolution.hpp"

// #include "BreakPartialSolution.hpp"

// #include "problems/PostListDecomposeSubproblem.hpp"

// #include "SackProblem.hpp"

// #include "PartialSolutionPathLabel.hpp"

using namespace std;

shared_ptr<P> PartialSolution::
	construct(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
		shared_ptr<SackItem> split_sack_item,
		shared_ptr<B> break_partial_solution,
		longdouble base_loss_value,
		shared_ptr<list<shared_ptr<P>>> constituent_partial_solutions) {
	shared_ptr<PartialSolution> partial_solution =
			shared_ptr<PartialSolution>(new PartialSolution(split_sack_item,
					constituent_partial_solutions));
	partial_solution->addSackItems(sack_items, break_partial_solution);
	// cout << "# of included items: " + to_string(sack_items->size()) << endl;
	shared_ptr<IdentifierOrderedSackItemTree> tree =
			partial_solution->_getIdentifierOrderedSackItemTree();
	// cout << "# of items added to tree: " + to_string(tree->getNumEntries()) << endl;
	return partial_solution;
}
shared_ptr<P> PartialSolution::
	_combinePartialSolutions(shared_ptr<P> partial_solution1,
		shared_ptr<P> partial_solution2, shared_ptr<SackItem> split_sack_item,
		shared_ptr<B> break_partial_solution, shared_ptr<SackProblem> problem1,
		shared_ptr<SackProblem> problem2) {
	// cout << "partial solution one: " + *(partial_solution1->toString()) << endl;
	// cout << "partial_solution two: " + *(partial_solution2->toString()) << endl;
	shared_ptr<list<shared_ptr<SackItem>>> sack_items1 = partial_solution1->getSackItems();
	shared_ptr<list<shared_ptr<SackItem>>> sack_items2 = partial_solution2->getSackItems();
	// cout << "number of items in collection one: " + to_string(sack_items1->size()) << endl;
	// cout << "number of items in collection two: " + to_string(sack_items2->size()) << endl;
	// cout << sack_items2->size() << endl;

	// must partially anticipate amount of space
	// necessary for set union of items from two lists

	/*
	vector<SackItem *> *sack_item_vector1 = new vector<SackItem *>();
	vector<SackItem *> *sack_item_vector2 = new vector<SackItem *>();
	for_each(sack_items1->begin(), sack_items2->end(),
			[&] (SackItem *a) { sack_item_vector1->push_back(a); });
	for_each(sack_items2->begin(), sack_items2->end(),
			[&] (SackItem *a) { sack_item_vector2->push_back()}
	*/
	shared_ptr<set<shared_ptr<SackItem>>> sack_item_set1 =
			shared_ptr<set<shared_ptr<SackItem>>>(new set<shared_ptr<SackItem>>());
	shared_ptr<set<shared_ptr<SackItem>>> sack_item_set2 =
			shared_ptr<set<shared_ptr<SackItem>>>(new set<shared_ptr<SackItem>>());
	for_each(sack_items1->begin(), sack_items1->end(),
			[&] (shared_ptr<SackItem> a) { sack_item_set1->insert(a); });
	for_each(sack_items2->begin(), sack_items2->end(),
			[&] (shared_ptr<SackItem> a) { sack_item_set2->insert(a); });

	// cout << "number of items in collection one pre-union: " + to_string(sack_item_set1->size()) << endl;
	// cout << "number of items in collection two pre-union: " + to_string(sack_item_set2->size()) << endl;
	shared_ptr<list<shared_ptr<SackItem>>> sack_item_set_union_list =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	// make room for intersection
	sack_item_set_union_list->resize(sack_items1->size() + sack_items2->size(), NULL);

	set_union(sack_item_set1->begin(), sack_item_set1->end(),
			sack_item_set2->begin(), sack_item_set2->end(),
			sack_item_set_union_list->begin());
	sack_item_set_union_list->erase(remove_if(sack_item_set_union_list->begin(),
			sack_item_set_union_list->end(),
			[&] (shared_ptr<SackItem> a) { return a == NULL; }),
			sack_item_set_union_list->end());
	shared_ptr<list<shared_ptr<SackItem>>> combined_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*sack_item_set_union_list));
	// cout << "number of items after union: " + to_string(combined_sack_items->size()) << endl;
	// possibly unnecessary
	shared_ptr<set<shared_ptr<SackItem>>> sack_item_set_union =
			shared_ptr<set<shared_ptr<SackItem>>>(new set<shared_ptr<SackItem>>());
	for_each(sack_item_set_union_list->begin(),
			sack_item_set_union_list->end(),
			[&] (shared_ptr<SackItem> a)
			{ sack_item_set_union->insert(a); });
	shared_ptr<list<shared_ptr<SackItem>>> patched_up_loss_contributors1 =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items1));
	patched_up_loss_contributors1->
			erase(remove_if(patched_up_loss_contributors1->begin(),
			patched_up_loss_contributors1->end(),
			[&] (shared_ptr<SackItem> a)
			{ return break_partial_solution->hasSackItem(a) == false; }),
					patched_up_loss_contributors1->end());
	shared_ptr<list<shared_ptr<SackItem>>> patched_up_loss_contributors2 =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items2));
	patched_up_loss_contributors2->
			erase(remove_if(patched_up_loss_contributors2->begin(),
			patched_up_loss_contributors2->end(),
			[&] (shared_ptr<SackItem> a)
			{ return break_partial_solution->hasSackItem(a) == false; }),
					patched_up_loss_contributors2->end());
	shared_ptr<list<shared_ptr<longdouble>>> patched_up_loss_values1 =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	patched_up_loss_values1->resize(patched_up_loss_contributors1->size(), NULL);
	transform(patched_up_loss_contributors1->begin(),
			patched_up_loss_contributors1->end(),
			patched_up_loss_values1->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
	shared_ptr<list<shared_ptr<longdouble>>> patched_up_loss_values2 =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	patched_up_loss_values2->resize(patched_up_loss_contributors2->size(), NULL);
	transform(patched_up_loss_contributors2->begin(),
			patched_up_loss_contributors2->end(),
			patched_up_loss_values2->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
	shared_ptr<longdouble> patched_up_loss_contribution1 =
			accumulate(patched_up_loss_values1->begin(), patched_up_loss_values1->end(),
					shared_ptr<longdouble>(new longdouble(0)),
					[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
					{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	shared_ptr<longdouble> patched_up_loss_contribution2 =
			accumulate(patched_up_loss_values2->begin(), patched_up_loss_values2->end(),
					shared_ptr<longdouble>(new longdouble(0)),
					[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
					{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	longdouble next_patched_up_loss_contribution1 = *patched_up_loss_contribution1;
	longdouble next_patched_up_loss_contribution2 = *patched_up_loss_contribution2;
	longdouble base_loss_value = partial_solution1->getBaseLossValue() +
			partial_solution2->getBaseLossValue() - next_patched_up_loss_contribution1
			- next_patched_up_loss_contribution2;
	shared_ptr<list<shared_ptr<PartialSolution>>> constituent_partial_solutions =
			shared_ptr<list<shared_ptr<PartialSolution>>>(new list<shared_ptr<PartialSolution>>());
	constituent_partial_solutions->push_back(partial_solution1);
	constituent_partial_solutions->push_back(partial_solution2);
	shared_ptr<PartialSolution> partial_solution =
			PartialSolution::construct(combined_sack_items,
					split_sack_item, break_partial_solution,
					base_loss_value, constituent_partial_solutions);
	// cout << "combined partial solution profit: " + to_string(partial_solution->getTotalProfit()) << endl;
	return partial_solution;
}

shared_ptr<list<shared_ptr<PartialSolution>>> PartialSolution::getConstituentPartialSolutions() {
	return this->constituent_partial_solutions;
}

shared_ptr<IdentifierOrderedSackItemTree> PartialSolution::_getIdentifierOrderedSackItemTree() {
	return this->identifier_ordered_sack_item_tree;
}

shared_ptr<list<shared_ptr<SackItem>>> PartialSolution::getSackItems() {

	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			this->sack_item_to_count_dict;

	shared_ptr<list<shared_ptr<SackItem>>> result =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());

	shared_ptr<pair<shared_ptr<SackItem>, shared_ptr<int>>> curr_pair;

	auto iterator = sack_item_to_count_dict->begin();

	while(iterator != sack_item_to_count_dict->end()) {
		pair<shared_ptr<SackItem>, shared_ptr<int>> curr_pair = *iterator;
		shared_ptr<SackItem> sack_item;
		shared_ptr<int> count;
		tie(sack_item, count) = curr_pair;
		result->push_back(sack_item);
		advance(iterator, 1);
	}
	return result;
}

shared_ptr<SackItem> PartialSolution::_getSplitSackItem() {
	return this->split_sack_item;
}

longlong PartialSolution::getTotalProfit() {
	return this->total_profit;
}

int PartialSolution::getTotalWeight() {
	return this->total_weight;
}

longdouble PartialSolution::getBaseLossValue() {
	return this->base_loss_value;
}

longdouble PartialSolution::getNonBaseLossValue() {
	return this->non_base_loss_value;
}

longdouble PartialSolution::getTotalLossValue() {
	longdouble base_loss_value = this->getBaseLossValue();
	longdouble non_base_loss_value = this->getNonBaseLossValue();
	longdouble total_loss_value = base_loss_value + non_base_loss_value;
	return total_loss_value;
}

void PartialSolution::setTotalProfit(longlong profit) {
	this->total_profit = profit;
}

void PartialSolution::setTotalWeight(int weight) {
	this->total_weight = weight;
}

void PartialSolution::setNonBaseLossValue(longdouble loss_value) {
	this->non_base_loss_value = loss_value;
}

void PartialSolution::addSackItem(shared_ptr<SackItem> sack_item,
		shared_ptr<BreakPartialSolution> break_partial_solution) {
	longlong profit = sack_item->getProfit();
	int weight = sack_item->getWeight();
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	longdouble loss_value;
	if (break_partial_solution->hasSackItem(sack_item) == true) {
		loss_value = 0;
	} else {
		loss_value = sack_item->getLossValue(split_sack_item, true);
	}
	longlong total_profit = this->getTotalProfit();
	int total_weight = this->getTotalWeight();
	longdouble non_base_loss_value = this->getNonBaseLossValue();
	longlong next_total_profit = total_profit + profit;
	int next_total_weight = total_weight + weight;
	longdouble next_non_base_loss_value = non_base_loss_value + loss_value;
	this->setTotalProfit(next_total_profit);
	this->setTotalWeight(next_total_weight);
	this->setNonBaseLossValue(next_non_base_loss_value);
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			this->sack_item_to_count_dict;
	// auto result = sack_item_to_count_dict->find(sack_item);
	// if (result == sack_item_to_count_dict->end()) {
	if (sack_item_to_count_dict->count(sack_item) == 0) {
		shared_ptr<pair<shared_ptr<SackItem>, shared_ptr<int>>> pair_to_insert =
					shared_ptr<pair<shared_ptr<SackItem>, shared_ptr<int>>>(new
							pair<shared_ptr<SackItem>, shared_ptr<int>>(sack_item,
									shared_ptr<int>(new int(1))));
		// did not encounter item
		sack_item_to_count_dict->insert(*pair_to_insert);
	}
	shared_ptr<U> identifier_ordered_sack_item_tree =
			this->_getIdentifierOrderedSackItemTree();
	identifier_ordered_sack_item_tree->insertSackItem(sack_item);
	this->sack_item_count = this->sack_item_count + 1;
}

// sack_item is a break partial solution sack item

void PartialSolution::
	undoAddSackItem(shared_ptr<SackItem> sack_item) {
	// cout << "undo adding a sack item: " + *(sack_item->toString()) << endl;
	longlong profit = sack_item->getProfit();
	int weight = sack_item->getWeight();
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	longdouble loss_value = sack_item->getLossValue(split_sack_item, true);
	longlong total_profit = this->getTotalProfit();
	int total_weight = this->getTotalWeight();
	longdouble non_base_loss_value = this->getNonBaseLossValue();
	longlong next_total_profit = total_profit - profit;
	int next_total_weight = total_weight - weight;
	longdouble next_non_base_loss_value = non_base_loss_value + loss_value;
	this->setTotalProfit(next_total_profit);
	this->setTotalWeight(next_total_weight);
	this->setNonBaseLossValue(next_non_base_loss_value);
	shared_ptr<unordered_map<shared_ptr<SackItem>,
		shared_ptr<int>>> sack_item_to_count_dict =
			this->sack_item_to_count_dict;
	sack_item_to_count_dict->erase(sack_item);
	shared_ptr<U> identifier_ordered_sack_item_tree =
			this->_getIdentifierOrderedSackItemTree();
	identifier_ordered_sack_item_tree->removeSackItem(sack_item->getIDValue());
	this->sack_item_count = this->sack_item_count - 1;
}

shared_ptr<PartialSolution> PartialSolution::clone(shared_ptr<BreakPartialSolution> break_partial_solution) {
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	longlong total_profit = this->getTotalProfit();
	int total_weight = this->getTotalWeight();
	longdouble base_loss_value = this->getBaseLossValue();
	longdouble non_base_loss_value = this->getNonBaseLossValue();
	shared_ptr<list<shared_ptr<SackItem>>> sack_items = this->getSackItems();
	shared_ptr<list<shared_ptr<SackItem>>> next_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items));
	shared_ptr<list<shared_ptr<PartialSolution>>> constituent_partial_solutions =
			this->getConstituentPartialSolutions();
	shared_ptr<list<shared_ptr<PartialSolution>>> next_constituent_partial_solutions =
			shared_ptr<list<shared_ptr<PartialSolution>>>(new
					list<shared_ptr<PartialSolution>>(*constituent_partial_solutions));
	shared_ptr<PartialSolution> partial_solution =
			shared_ptr<PartialSolution>(new PartialSolution(split_sack_item,
					next_constituent_partial_solutions));
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			shared_ptr<unordered_map<shared_ptr<SackItem>,
			shared_ptr<int>>>(new unordered_map<shared_ptr<SackItem>,
					shared_ptr<int>>());
	// new unordered_map<SackItem *, int *>(5);
	// deal with bug relating to empty unordered map
	// sack_item_to_count_dict->insert(*(new pair<SackItem *, int *>(NULL, NULL)));
	for (shared_ptr<SackItem> curr_sack_item : *sack_items) {
		shared_ptr<pair<shared_ptr<SackItem>, shared_ptr<int>>> pair_to_insert =
				shared_ptr<pair<shared_ptr<SackItem>, shared_ptr<int>>>(new
						pair<shared_ptr<SackItem>, shared_ptr<int>>(curr_sack_item,
								shared_ptr<int>(new int(1))));
		sack_item_to_count_dict->insert(*pair_to_insert);
	}
	shared_ptr<U> identifier_ordered_sack_item_tree =
			this->_getIdentifierOrderedSackItemTree();
	shared_ptr<U> next_tree = identifier_ordered_sack_item_tree->clone();
	int sack_item_count = this->sack_item_count;
	partial_solution->total_profit = total_profit;
	partial_solution->total_weight = total_weight;
	partial_solution->non_base_loss_value = non_base_loss_value;
	partial_solution->sack_item_to_count_dict = sack_item_to_count_dict;
	partial_solution->identifier_ordered_sack_item_tree = next_tree;
	partial_solution->sack_item_count = sack_item_count;
	return partial_solution;
}

void PartialSolution::addSackItems(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
		shared_ptr<BreakPartialSolution> break_partial_solution) {
	// cout << "adding sack items to a partial solution" << endl;
for (shared_ptr<SackItem> sack_item : *sack_items) {
	this->addSackItem(sack_item, break_partial_solution);
}
}

bool PartialSolution::isFeasible(int capacity) {

	int weight = this->getTotalWeight();
	bool is_feasible = (weight <= capacity) && (weight >= 0);
	return is_feasible;

}

shared_ptr<string> PartialSolution::toString() {
	longlong total_profit = this->getTotalProfit();
	int total_weight = this->getTotalWeight();
	string result_str = "(" + to_string(total_profit) +
			", " + to_string(total_weight) + ")";
	shared_ptr<string> next_result_str =
			shared_ptr<string>(new string(result_str));
	return next_result_str;

}

shared_ptr<string> PartialSolution::toBareString(shared_ptr<PostListDecomposeSubproblem>
		post_list_decompose_subproblem,
		shared_ptr<BreakPartialSolution> break_partial_solution) {
	shared_ptr<list<shared_ptr<SackItem>>> sack_items =
			this->getSackItems();
	shared_ptr<list<shared_ptr<SackItem>>> next_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items));
	remove_if(next_sack_items->begin(), next_sack_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ return post_list_decompose_subproblem->hasSackItem(a) == false; });
	shared_ptr<list<int>> weight_values =
			shared_ptr<list<int>>(new list<int>());
	weight_values->resize(next_sack_items->size());
	transform(next_sack_items->begin(), next_sack_items->end(),
			weight_values->begin(),
			[&] (shared_ptr<SackItem> a) { return a->getWeight(); });
	shared_ptr<list<longlong>> profit_values =
			shared_ptr<list<longlong>>(new list<longlong>());
	profit_values->resize(next_sack_items->size());
	transform(next_sack_items->begin(), next_sack_items->end(),
			profit_values->begin(),
			[&] (shared_ptr<SackItem> a) { return a->getProfit(); });
	int total_weight = accumulate(weight_values->begin(), weight_values->end(),
			0, [&] (int a, int b) { return a + b; });
	longlong total_profit = accumulate(profit_values->begin(), profit_values->end(),
			0, [&] (longlong a, longlong b) { return a + b; });
	string result_str = "(" + to_string(total_profit) + ", " + to_string(total_weight) + ")";
	shared_ptr<string> next_result_str =
			shared_ptr<string>(new string(result_str));
	return next_result_str;
}

shared_ptr<string> PartialSolution::toExtendedString() {
	shared_ptr<list<shared_ptr<SackItem>>> sack_items =
			this->getSackItems();
	shared_ptr<string> result_str =
			shared_ptr<string>(new string(""));
	for_each(sack_items->begin(), sack_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ result_str = shared_ptr<string>(new string(*result_str + *(a->toString()))); });
	return result_str;
}

bool PartialSolution::hasSackItem(shared_ptr<SackItem> sack_item) {
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			this->sack_item_to_count_dict;
	/*
	bool has_sack_item =
			sack_item_to_count_dict->find(sack_item)
			!= sack_item_to_count_dict->end();
	*/
	// cout << "bucket count: " + to_string(sack_item_to_count_dict->bucket_count()) << endl;
	// sack_item_to_count_dict->insert(*(new pair<SackItem *, int *>(NULL, NULL)));
	// cout << "hash table size: " + to_string(sack_item_to_count_dict->size()) << endl;
	bool has_sack_item =
			sack_item_to_count_dict->count(sack_item) != 0;
	return has_sack_item;
}

int PartialSolution::getNumSackItems() {
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			this->sack_item_to_count_dict;
	int num_sack_items = sack_item_to_count_dict->size();
	return num_sack_items;
}

shared_ptr<list<shared_ptr<SackItem>>> PartialSolution::getItemsOrderedByIdentifierValue() {
	shared_ptr<U> identifier_ordered_sack_item_tree =
			this->_getIdentifierOrderedSackItemTree();
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items =
			identifier_ordered_sack_item_tree
			->toIdentifierOrderedSackItemList();
	return sorted_sack_items;
}

shared_ptr<PartialSolutionPathLabel> PartialSolution::toPartialSolutionPathLabel() {
	shared_ptr<PartialSolutionPathLabel> path_label =
			shared_ptr<PartialSolutionPathLabel>(new PartialSolutionPathLabel(shared_from_this()));
	return path_label;
}

PartialSolution::PartialSolution(shared_ptr<SackItem> split_sack_item,
		shared_ptr<list<shared_ptr<PartialSolution>>> constituent_partial_solutions) {
	this->split_sack_item = split_sack_item;
	this->constituent_partial_solutions = constituent_partial_solutions;
	this->base_loss_value = 0;
	this->total_profit = 0;
	this->total_weight = 0;
	this->non_base_loss_value = 0;
	// this->sack_item_to_count_dict = new unordered_map<SackItem *, int *>(5);
	this->sack_item_to_count_dict =
			shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>>(new
					unordered_map<shared_ptr<SackItem>, shared_ptr<int>>());
	// cout << "inserting a key-value pair" << endl;
	// this->sack_item_to_count_dict->insert(*(new pair<SackItem *, int *>(NULL, NULL)));
	// cout << "next hash table size: " + to_string(this->sack_item_to_count_dict->size()) << endl;
	/*
	if (this->sack_item_to_count_dict->size() == 0) {
		throw "error";
	}
	*/
	shared_ptr<list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>> entries =
			shared_ptr<list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>>(new
					list<shared_ptr<tuple<int, shared_ptr<SackItem>>>>());
	this->identifier_ordered_sack_item_tree =
			IdentifierOrderedSackItemTree::construct(entries);
	this->sack_item_count = 0;
}

PartialSolution::~PartialSolution() {
	// cout << "destructing a partial solution" << endl;
	(this->split_sack_item).reset();
	(this->constituent_partial_solutions).reset();
	(this->sack_item_to_count_dict).reset();
	(this->identifier_ordered_sack_item_tree).reset();
	// cout << (this->identifier_ordered_sack_item_tree).use_count() << endl;
}

// #include "BreakPartialSolution.hpp"

class PartialSolution;

shared_ptr<BreakPartialSolution> BreakPartialSolution::
	construct(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
		shared_ptr<SackItem> split_sack_item) {
	shared_ptr<BreakPartialSolution> break_partial_solution =
			shared_ptr<BreakPartialSolution>(new BreakPartialSolution(split_sack_item));
	longdouble base_loss_value = 0;
	shared_ptr<list<longlong>> profit_values = shared_ptr<list<longlong>>(new list<longlong>());
	profit_values->resize(sack_items->size(), 0);
	transform(sack_items->begin(), sack_items->end(),
			profit_values->begin(),
			[&] (shared_ptr<SackItem> a) { return a->getProfit(); });
	longlong total_profit = accumulate(profit_values->begin(), profit_values->end(),
			0, [&] (longlong a, longlong b) { return a + b; });
	shared_ptr<list<int>> weight_values = shared_ptr<list<int>>(new list<int>());
	weight_values->resize(sack_items->size(), 0);
	transform(sack_items->begin(), sack_items->end(),
			weight_values->begin(),
			[&] (shared_ptr<SackItem> a) { return a->getWeight(); });
	int total_weight = accumulate(weight_values->begin(), weight_values->end(),
			0, [&] (int a, int b) { return a + b; });
	longdouble non_base_loss_value = 0;
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>>(new
					unordered_map<shared_ptr<SackItem>, shared_ptr<int>>());
	// new unordered_map<SackItem *, int *>(5);
	// for dealing with a bug relating to empty map
	// sack_item_to_count_dict->insert(*(new pair<SackItem *, int *>(NULL, NULL)));
	for_each(sack_items->begin(), sack_items->end(),
			[&] (shared_ptr<SackItem> a) { sack_item_to_count_dict->
				insert(*(shared_ptr<pair<shared_ptr<SackItem>,
						shared_ptr<int>>>(new pair<shared_ptr<SackItem>,
								shared_ptr<int>>(a, shared_ptr<int>(new int(1)))))); });
	shared_ptr<IdentifierOrderedSackItemTree> identifier_ordered_sack_item_tree =
			IdentifierOrderedSackItemTree::
			construct(shared_ptr<list<shared_ptr<tuple<int,
					shared_ptr<SackItem>>>>>(new list<shared_ptr<tuple<int,
							shared_ptr<SackItem>>>>()));
	for_each(sack_items->begin(), sack_items->end(),
			[&] (shared_ptr<SackItem> a) { identifier_ordered_sack_item_tree->insertSackItem(a); });
	break_partial_solution->total_profit = total_profit;
	break_partial_solution->total_weight = total_weight;
	break_partial_solution->base_loss_value = base_loss_value;
	break_partial_solution->non_base_loss_value = non_base_loss_value;
	break_partial_solution->sack_item_to_count_dict = sack_item_to_count_dict;
	break_partial_solution->identifier_ordered_sack_item_tree =
			identifier_ordered_sack_item_tree;
	return break_partial_solution;
}

shared_ptr<PartialSolution> BreakPartialSolution::
	clone(shared_ptr<BreakPartialSolution> break_partial_solution) {
	shared_ptr<PartialSolution> result = PartialSolution::clone(break_partial_solution);
	return result;
}

BreakPartialSolution::BreakPartialSolution(shared_ptr<SackItem> split_sack_item)
	: PartialSolution(split_sack_item,
			shared_ptr<list<shared_ptr<PartialSolution>>>(new list<shared_ptr<PartialSolution>>())) {
	return;
}

BreakPartialSolution::~BreakPartialSolution() {
	return;
}


// #include "PartialSolutionPathLabel.hpp"

using A = PartialSolutionPathLabel;

int PartialSolutionPathLabel::comp(shared_ptr<A> a, shared_ptr<A> b) {
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items1 =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*(a->_getSortedSackItems())));
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items2 =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*(b->_getSortedSackItems())));
	int result =
			PartialSolutionPathLabel::
				compHelper(sorted_sack_items1, sorted_sack_items2);
	return result;
}

int PartialSolutionPathLabel::compHelper(shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items1,
		shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items2) {
	bool have_next_sack_item1 = sorted_sack_items1->size() != 0;
	bool have_next_sack_item2 = sorted_sack_items2->size() != 0;
	if ((have_next_sack_item1 == false) && (have_next_sack_item2 == false)) {
		return 0;
	} else if ((have_next_sack_item1 == true) && (have_next_sack_item2 == false)) {
		return 1;
	} else if ((have_next_sack_item1 == false) && (have_next_sack_item2 == true)) {
		return -1;
	} else {
		// ((have_next_sack_item1 == true) && (have_next_sack_item2 == true))
		shared_ptr<SackItem> next_sack_item1 = sorted_sack_items1->front();
		shared_ptr<SackItem> next_sack_item2 = sorted_sack_items2->front();
		int next_sack_item_identifier_value1 = next_sack_item1->getIDValue();
		int next_sack_item_identifier_value2 = next_sack_item2->getIDValue();
		shared_ptr<list<shared_ptr<SackItem>>> next_sack_items1 = sorted_sack_items1;
		next_sack_items1->pop_front();
		shared_ptr<list<shared_ptr<SackItem>>> next_sack_items2 = sorted_sack_items2;
		next_sack_items2->pop_front();
		int comp_result = Util::comp(next_sack_item_identifier_value1, next_sack_item_identifier_value2);
		// cout << comp_result << endl;
		if (comp_result == 0) {
			return PartialSolutionPathLabel::
					compHelper(next_sack_items1, next_sack_items2);
		} else {
			return comp_result;
		}

	}
}

shared_ptr<A> PartialSolutionPathLabel::getMin(shared_ptr<list<shared_ptr<A>>> partial_solution_path_labels) {
	if (partial_solution_path_labels->size() == 0) {
		return NULL;
	} else {
		shared_ptr<list<shared_ptr<A>>> next_partial_solution_path_labels =
				shared_ptr<list<shared_ptr<A>>>(new
						list<shared_ptr<A>>(*partial_solution_path_labels));
		shared_ptr<PartialSolutionPathLabel> curr_partial_solution_path_label =
				next_partial_solution_path_labels->front();
		shared_ptr<PartialSolutionPathLabel> curr_min =
				curr_partial_solution_path_label;
		shared_ptr<list<shared_ptr<A>>> next_next_partial_solution_path_labels =
				next_partial_solution_path_labels;
		next_next_partial_solution_path_labels->pop_front();
		shared_ptr<A> result = PartialSolutionPathLabel::
				getMinHelper(next_next_partial_solution_path_labels, curr_min);
		shared_ptr<list<shared_ptr<SackItem>>> sack_items = result->_getSortedSackItems();
		// cout << "winning path label sack items:" << endl;
		/*
		for_each(sack_items->begin(), sack_items->end(),
				[&] (SackItem *a) { cout << *(a->toString()) << endl; });
		*/
		return result;
	}
	}

shared_ptr<A> PartialSolutionPathLabel::getMinHelper(shared_ptr<list<shared_ptr<A>>> partial_solution_path_labels,
		shared_ptr<A> curr_min) {
	if (partial_solution_path_labels->size() == 0) {
		return curr_min;
	} else {
		shared_ptr<PartialSolutionPathLabel> curr_partial_solution_path_label =
				partial_solution_path_labels->front();
		shared_ptr<PartialSolutionPathLabel> next_min;
		shared_ptr<list<shared_ptr<PartialSolutionPathLabel>>> next_partial_solution_path_labels =
				partial_solution_path_labels;
		next_partial_solution_path_labels->pop_front();
		int comp_result = PartialSolutionPathLabel::
				comp(curr_partial_solution_path_label, curr_min);
		if ((comp_result == 0) || (comp_result == -1)) {
			next_min = curr_partial_solution_path_label;
		} else {
			next_min = curr_min;
		}
		return PartialSolutionPathLabel::
				getMinHelper(next_partial_solution_path_labels, next_min);
	}
}

shared_ptr<A> PartialSolutionPathLabel::_combinePathLabels(shared_ptr<A> path_label1,
		shared_ptr<A> path_label2,
		shared_ptr<SackItem> split_sack_item,
		shared_ptr<BreakPartialSolution> break_partial_solution,
		shared_ptr<SackProblem> problem1, shared_ptr<SackProblem> problem2) {
	shared_ptr<PartialSolution> partial_solution1 = (path_label1->partial_solution).lock();
	shared_ptr<PartialSolution> partial_solution2 = (path_label2->partial_solution).lock();
	shared_ptr<PartialSolution> combined_partial_solution =
			PartialSolution::_combinePartialSolutions(partial_solution1,
					partial_solution2, split_sack_item, break_partial_solution,
					problem1, problem2);
	shared_ptr<PartialSolutionPathLabel> path_label =
			combined_partial_solution->toPartialSolutionPathLabel();
	return path_label;
}

shared_ptr<PartialSolution> PartialSolutionPathLabel::_getPartialSolution() {
	return (this->partial_solution).lock();
}

shared_ptr<list<shared_ptr<SackItem>>> PartialSolutionPathLabel::_getSortedSackItems() {
	return this->sorted_sack_items;
}

bool PartialSolutionPathLabel::isEqualTo(shared_ptr<A> path_label) {
	int comparison = PartialSolutionPathLabel::comp(shared_from_this(), path_label);
	bool result = comparison == 0;
	// cout << result << endl;
	return result;
}

PartialSolutionPathLabel::PartialSolutionPathLabel(shared_ptr<PartialSolution> partial_solution) {
	this->partial_solution = partial_solution;
	this->sorted_sack_items =
			this->_getPartialSolution()->getItemsOrderedByIdentifierValue();
}

PartialSolutionPathLabel::~PartialSolutionPathLabel() {
	// cout << "destructing a partial solution path label" << endl;
	(this->partial_solution).reset();
	(this->sorted_sack_items).reset();
}

// #include "ListDecomposition.hpp"

// #include "../util/Util.hpp"

// #include "SackItem.hpp"

// #include "PartialSolutionPathLabel.hpp"

using P = PartialSolution;

using A = PartialSolutionPathLabel;

// tests additionally depend on NonCoreSackSubproblem,
// SackProblem, SackSubproblem, PartialSolution,
// BreakPartialSolution, PartialSolutionPathLabel

void ListDecomposition::ponder(int n) {

	// groupByWeight allows us to retrieve
	// a collection of partial solutions
	// grouped by weight in time linear in n

	int W = 3;

	shared_ptr<SackItem> sack_item1 = shared_ptr<SackItem>(new SackItem(2, 1, 1));
	shared_ptr<SackItem> sack_item2 = shared_ptr<SackItem>(new SackItem(3, 1, 2));
	shared_ptr<SackItem> sack_item3 = shared_ptr<SackItem>(new SackItem(4, 1, 3));
	shared_ptr<SackItem> sack_item4 = shared_ptr<SackItem>(new SackItem(1, 1, 4));
	shared_ptr<SackItem> sack_item5 = shared_ptr<SackItem>(new SackItem(1, 1, 5));
	shared_ptr<SackItem> sack_item6 = shared_ptr<SackItem>(new SackItem(2, 1, 6));
	// share ownership
	shared_ptr<SackItem> split_sack_item = shared_ptr<SackItem>(sack_item4);
	shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	break_partial_solution_sack_items->push_back(sack_item1);
	break_partial_solution_sack_items->push_back(sack_item2);
	break_partial_solution_sack_items->push_back(sack_item3);
	shared_ptr<BreakPartialSolution> break_partial_solution =
			BreakPartialSolution::construct(break_partial_solution_sack_items,
					split_sack_item);
	shared_ptr<P> partial_solution1 =
			shared_ptr<PartialSolution>(new PartialSolution(split_sack_item, NULL));
	partial_solution1->addSackItem(sack_item1, break_partial_solution);
	shared_ptr<P> partial_solution2 = shared_ptr<P>(new PartialSolution(split_sack_item, NULL));
	partial_solution2->addSackItem(sack_item2, break_partial_solution);
	shared_ptr<P> partial_solution3 = shared_ptr<P>(new PartialSolution(split_sack_item, NULL));
	partial_solution3->addSackItem(sack_item4, break_partial_solution);
	partial_solution3->addSackItem(sack_item5, break_partial_solution);
	partial_solution3->addSackItem(sack_item6, break_partial_solution);
	shared_ptr<list<shared_ptr<P>>> partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	partial_solutions->push_back(partial_solution1);
	partial_solutions->push_back(partial_solution2);
	partial_solutions->push_back(partial_solution3);
	shared_ptr<list<shared_ptr<list<shared_ptr<P>>>>> result =
			ListDecomposition::groupByWeight(partial_solutions);
	shared_ptr<string> result_str_list_list = shared_ptr<string>(new string(""));
	for(shared_ptr<list<shared_ptr<P>>> partial_solution_list : *result) {
		for (shared_ptr<P> partial_solution : *partial_solution_list) {
			shared_ptr<string> curr_str = partial_solution->toString();
			result_str_list_list = shared_ptr<string>(new string(*result_str_list_list + *curr_str + " "));
		}
		result_str_list_list = shared_ptr<string>(new string(*result_str_list_list + "\n"));
	}
	cout << *result_str_list_list << endl;

	// expect a group of (3, 1) and (2, 1),
	// then a group of (4, 3)

	// getMaxScoreValuesGivenMaxWeight
	// allows us to cumulatively determine
	// max. score for a given max. weight
	// given a collection of items
	// sorted by weight in time linear in n

	shared_ptr<list<shared_ptr<SackItem>>> sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());

	shared_ptr<NonCoreSackSubproblem> non_core_subproblem =
			shared_ptr<NonCoreSackSubproblem>(new NonCoreSackSubproblem(NULL,
					sack_items, W, break_partial_solution));
	non_core_subproblem->init();

	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> next_result =
			ListDecomposition::getMaxScoreValuesGivenMaxWeight(partial_solutions,
					non_core_subproblem);

	for_each(next_result->begin(), next_result->end(),
			[&] (shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> a)
			{ cout << to_string(*(get<0>(*a))) << " "; });

	// expect 3, 3, 4

	cout << "\n";

	// getResidualCapacitiesGivenPartialSolutions
	// allows us to determine values for remaining space
	// given an ordered collection of items
	// in time linear in n

	shared_ptr<list<shared_ptr<int>>> next_next_result =
			ListDecomposition::
			getResidualCapacitiesGivenPartialSolutions(partial_solutions, W);

	for_each(next_next_result->begin(), next_next_result->end(),
			[&] (shared_ptr<int> a)
			{ cout << to_string(*a) << " "; });

	cout << "\n";

	// expect 2, 2, 0

	// getClosestFeasibleWeightValuesGivenResidualCapacities
	// allows us to retrieve closest actual max. feasible weight value
	// given residual capacities in time linear in n

	shared_ptr<list<shared_ptr<int>>> weight_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	weight_values->push_back(shared_ptr<int>(new int(sack_item3->getWeight())));

	shared_ptr<list<shared_ptr<int>>> result4 = ListDecomposition::
		getClosestFeasibleWeightValuesGivenResidualCapacities(next_next_result,
			weight_values);

	for_each(result4->begin(), result4->end(),
			[&] (shared_ptr<int> a)
			{ cout << to_string(*a) << " "; });

	cout << "\n";

	// expect 1, 1, 1

	// getABestPair allows us to retrieve an item from a "left" collection
	// and an item from a "right" collection s.t. the combination is feasible
	// and has highest score in time linear in n and m

	shared_ptr<P> empty_left_partial_solution =
			shared_ptr<P>(new PartialSolution(split_sack_item, NULL));
	shared_ptr<P> empty_right_partial_solution =
			shared_ptr<P>(new PartialSolution(split_sack_item, NULL));

	shared_ptr<list<shared_ptr<P>>> left_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	left_partial_solutions->push_back(empty_left_partial_solution);
	left_partial_solutions->push_back(partial_solution1);
	left_partial_solutions->push_back(partial_solution2);
	shared_ptr<list<shared_ptr<P>>> right_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	right_partial_solutions->push_back(empty_right_partial_solution);
	right_partial_solutions->push_back(partial_solution3);

	shared_ptr<list<shared_ptr<SackItem>>> left_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	left_sack_items->push_back(sack_item1);
	left_sack_items->push_back(sack_item2);
	left_sack_items->push_back(sack_item3);

	shared_ptr<list<shared_ptr<SackItem>>> right_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	right_sack_items->push_back(sack_item4);
	right_sack_items->push_back(sack_item5);
	right_sack_items->push_back(sack_item6);

	int capacity = W;
	shared_ptr<NonCoreSackSubproblem> next_non_core_subproblem = non_core_subproblem;
	shared_ptr<PostListDecomposeSubproblem> left_problem =
			shared_ptr<PostListDecomposeSubproblem>(new
					PostListDecomposeSubproblem(NULL, left_sack_items, W, NULL, true));
	left_problem->init();
	shared_ptr<PostListDecomposeSubproblem> right_problem =
			shared_ptr<PostListDecomposeSubproblem>(new
					PostListDecomposeSubproblem(NULL, right_sack_items, W, NULL, false));
	right_problem->init();

	shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>> result5 =
			ListDecomposition::getABestPair(left_partial_solutions,
			right_partial_solutions, capacity, next_non_core_subproblem,
			left_problem, right_problem);

	shared_ptr<P> left_partial_solution;
	shared_ptr<P> right_partial_solution;
	tie(left_partial_solution, right_partial_solution) = *result5;

	cout << *(left_partial_solution->toString()) << endl;
	cout << *(right_partial_solution->toString()) << endl;

	// expect (0, 0) and (4, 3)

}

shared_ptr<list<shared_ptr<list<shared_ptr<P>>>>> ListDecomposition::
	groupByWeight(shared_ptr<list<shared_ptr<P>>> partial_solutions) {

shared_ptr<list<shared_ptr<int>>> ordered_weight_values =
		shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
ordered_weight_values->resize(partial_solutions->size());
transform(partial_solutions->begin(), partial_solutions->end(),
		ordered_weight_values->begin(),
		[&] (shared_ptr<P> a) { return shared_ptr<int>(new int(a->getTotalWeight())); });
shared_ptr<list<shared_ptr<int>>> ordered_distinct_weight_values =
		Util::removeDuplicateValuesGivenSortedValues(ordered_weight_values);
shared_ptr<Dictionary<int, PartialSolution>> weight_to_partial_solution_dict =
		shared_ptr<Dictionary<int, PartialSolution>>(new Dictionary<int, PartialSolution>());
for (shared_ptr<P> partial_solution : *partial_solutions) {
	int weight = partial_solution->getTotalWeight();
	weight_to_partial_solution_dict->insert(shared_ptr<int>(new int(weight)), partial_solution);
}
shared_ptr<list<shared_ptr<list<shared_ptr<P>>>>> partial_solution_list =
		shared_ptr<list<shared_ptr<list<shared_ptr<P>>>>>(new list<shared_ptr<list<shared_ptr<P>>>>());
for (shared_ptr<int> weight : *ordered_distinct_weight_values) {
	shared_ptr<list<shared_ptr<tuple<shared_ptr<int>, shared_ptr<P>>>>> weight_to_partial_solution_pairs =
			weight_to_partial_solution_dict->findAll(weight);
shared_ptr<list<shared_ptr<P>>> curr_partial_solutions =
		shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
for_each(weight_to_partial_solution_pairs->begin(),
		weight_to_partial_solution_pairs->end(),
		[&] (shared_ptr<tuple<shared_ptr<int>, shared_ptr<P>>> a)
		{ curr_partial_solutions->push_back(get<1>(*a)); });
	partial_solution_list->push_back(curr_partial_solutions);
}
return partial_solution_list;
}

shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> ListDecomposition::
	getMaxScoreValuesGivenMaxWeight(shared_ptr<list<shared_ptr<P>>> partial_solutions,
		shared_ptr<NonCoreSackSubproblem> non_core_subproblem) {
	// update partial solution collection so as to have
	// best scores for given particular weight values
	shared_ptr<list<shared_ptr<list<shared_ptr<P>>>>> grouped_partial_solutions =
			ListDecomposition::groupByWeight(partial_solutions);
	shared_ptr<list<shared_ptr<P>>> updated_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	for (shared_ptr<list<shared_ptr<P>>> partial_solution_group : *grouped_partial_solutions) {
		shared_ptr<list<shared_ptr<longlong>>> profit_values =
				shared_ptr<list<shared_ptr<longlong>>>(new list<shared_ptr<longlong>>());
		profit_values->resize(partial_solution_group->size(), NULL);
		transform(partial_solution_group->begin(), partial_solution_group->end(),
				profit_values->begin(),
				[&] (shared_ptr<P> a) { return shared_ptr<longlong>(new longlong(a->getTotalProfit())); });
		int num_partial_solutions = partial_solution_group->size();
		shared_ptr<longlong> max_profit_value = accumulate(profit_values->begin(),
				profit_values->end(), shared_ptr<longlong>(new longlong(0)),
				[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
				{ return (*a > *b) ? a : b; });
		longlong next_max_profit_value = *max_profit_value;
		shared_ptr<list<shared_ptr<P>>> candidate_partial_solutions =
				shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*partial_solution_group));
		candidate_partial_solutions->erase(remove_if(candidate_partial_solutions->begin(),
				candidate_partial_solutions->end(),
				[&] (shared_ptr<P> a)
				{ return (a->getTotalProfit() == next_max_profit_value) == false; }),
				candidate_partial_solutions->end());
		shared_ptr<list<shared_ptr<A>>> path_labels =
				shared_ptr<list<shared_ptr<A>>>(new list<shared_ptr<A>>());
		path_labels->resize(candidate_partial_solutions->size(), NULL);
		transform(candidate_partial_solutions->begin(),
				candidate_partial_solutions->end(), path_labels->begin(),
				[&] (shared_ptr<P> a) { return a->toPartialSolutionPathLabel(); });
		shared_ptr<A> best_path_label =
				PartialSolutionPathLabel::getMin(path_labels);
		shared_ptr<list<shared_ptr<P>>> next_candidate_partial_solutions =
				shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*candidate_partial_solutions));
		next_candidate_partial_solutions
			->erase(remove_if(next_candidate_partial_solutions->begin(),
					next_candidate_partial_solutions->end(),
					[&] (shared_ptr<P> a)
					{ return ((a->toPartialSolutionPathLabel()->
							isEqualTo(best_path_label)) == false); }),
					next_candidate_partial_solutions->end());
		shared_ptr<P> chosen_partial_solution =
				next_candidate_partial_solutions->front();
		shared_ptr<list<shared_ptr<P>>> partial_solution_additions =
				shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
		partial_solution_additions->resize(num_partial_solutions, NULL);
		fill_n(partial_solution_additions->begin(),
				num_partial_solutions, chosen_partial_solution);
		updated_partial_solutions->splice(updated_partial_solutions->end(),
				*partial_solution_additions);
	}
	// retrieve cumulative best scores for current
	//   and previously seen weight values
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> tagged_max_score_values =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>());
	longlong curr_best_score_profit_value = 0;
	shared_ptr<A> curr_best_score_path_label = NULL;
	/*
	list<int *> *i_values = new list<int *>();
	i_values->resize(updated_partial_solutions->size(), NULL);
	iota(i_values->begin(), i_values->end(), 0);
	*/
	for (shared_ptr<P> partial_solution : *updated_partial_solutions) {
		shared_ptr<P> curr_partial_solution = partial_solution;
		longlong curr_profit_value = curr_partial_solution->getTotalProfit();
		shared_ptr<A> curr_path_label = curr_partial_solution->toPartialSolutionPathLabel();
		if (curr_profit_value == curr_best_score_profit_value) {
			// resolve tie
			if (curr_best_score_path_label == NULL) {
				curr_best_score_path_label = curr_path_label;
			} else {
				shared_ptr<list<shared_ptr<A>>> path_label_candidates =
						shared_ptr<list<shared_ptr<A>>>(new list<shared_ptr<A>>());
				path_label_candidates->push_back(curr_best_score_path_label);
				path_label_candidates->push_back(curr_path_label);
				shared_ptr<A> next_best_path_label = PartialSolutionPathLabel::
						getMin(path_label_candidates);
				curr_best_score_path_label = next_best_path_label;
			}
		} else if (curr_profit_value > curr_best_score_profit_value) {
			curr_best_score_profit_value = curr_profit_value;
			curr_best_score_path_label = curr_path_label;
		}
		shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> curr_max_score_value =
				shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>(new tuple<shared_ptr<longlong>,
						shared_ptr<A>>(shared_ptr<longlong>(new longlong(curr_best_score_profit_value)),
						curr_best_score_path_label));
		tagged_max_score_values->push_back(curr_max_score_value);
	}
	return tagged_max_score_values;
}

shared_ptr<list<shared_ptr<int>>> ListDecomposition::
	getResidualCapacitiesGivenPartialSolutions(shared_ptr<list<shared_ptr<P>>> partial_solutions,
		int capacity) {
	shared_ptr<list<shared_ptr<int>>> weight_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	weight_values->resize(partial_solutions->size(), NULL);
	transform(partial_solutions->begin(), partial_solutions->end(),
			weight_values->begin(),
			[&] (shared_ptr<P> a)
			{ return shared_ptr<int>(new int(a->getTotalWeight())); });
	shared_ptr<list<shared_ptr<int>>> residual_capacity_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	residual_capacity_values->resize(weight_values->size(), NULL);
	transform(weight_values->begin(), weight_values->end(),
			residual_capacity_values->begin(),
			[&] (shared_ptr<int> a) { return shared_ptr<int>(new int(capacity - *a)); });
	return residual_capacity_values;
}

shared_ptr<list<shared_ptr<int>>> ListDecomposition::
	getClosestFeasibleWeightValuesGivenResidualCapacities(shared_ptr<list<shared_ptr<int>>> residual_capacities,
		shared_ptr<list<shared_ptr<int>>> weight_values) {
	shared_ptr<list<shared_ptr<int>>> result = ListDecomposition::
		getClosestFeasibleWeightValuesGivenResidualCapacitiesHelper(residual_capacities,
		weight_values, 0, shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>()));
	return result;
}

shared_ptr<list<shared_ptr<int>>> ListDecomposition::
	getClosestFeasibleWeightValuesGivenResidualCapacitiesHelper(shared_ptr<list<shared_ptr<int>>> residual_capacities,
		shared_ptr<list<shared_ptr<int>>> weight_values, int prev_weight_value,
		shared_ptr<list<shared_ptr<int>>> closest_feasible_weight_values) {
	if (residual_capacities->size() == 0) {
		return closest_feasible_weight_values;
	} else if (weight_values->size() == 0) {
		shared_ptr<list<shared_ptr<int>>> next_residual_capacities = residual_capacities;
		next_residual_capacities->pop_front();
		shared_ptr<list<shared_ptr<int>>> next_weight_values = weight_values;
		int next_prev_weight_value = prev_weight_value;
		shared_ptr<list<shared_ptr<int>>> next_closest_feasible_weight_values =
				shared_ptr<list<shared_ptr<int>>>(closest_feasible_weight_values);
		next_closest_feasible_weight_values->push_back(shared_ptr<int>(new int(prev_weight_value)));
		return ListDecomposition::
				getClosestFeasibleWeightValuesGivenResidualCapacitiesHelper(next_residual_capacities,
						next_weight_values, next_prev_weight_value,
						next_closest_feasible_weight_values);
	} else {
		shared_ptr<int> curr_residual_capacity = residual_capacities->front();
		shared_ptr<int> curr_weight_value = weight_values->front();
		if (*curr_weight_value > *curr_residual_capacity) {
			shared_ptr<list<shared_ptr<int>>> next_residual_capacities = residual_capacities;
			next_residual_capacities->pop_front();
			shared_ptr<list<shared_ptr<int>>> next_weight_values = weight_values;
			int next_prev_weight_value = prev_weight_value;
			shared_ptr<list<shared_ptr<int>>> next_closest_feasible_weight_values =
					closest_feasible_weight_values;
			next_closest_feasible_weight_values->push_back(shared_ptr<int>(new int (prev_weight_value)));
			return ListDecomposition::
					getClosestFeasibleWeightValuesGivenResidualCapacitiesHelper(next_residual_capacities,
							next_weight_values, next_prev_weight_value,
							next_closest_feasible_weight_values);
		} else {
			shared_ptr<list<shared_ptr<int>>> next_residual_capacities =
					residual_capacities;
			shared_ptr<list<shared_ptr<int>>> next_weight_values = weight_values;
			next_weight_values->pop_front();
			int next_prev_weight_value = *curr_weight_value;
			shared_ptr<list<shared_ptr<int>>> next_closest_feasible_weight_values =
					closest_feasible_weight_values;
			return ListDecomposition::
					getClosestFeasibleWeightValuesGivenResidualCapacitiesHelper(next_residual_capacities,
							next_weight_values, next_prev_weight_value,
							next_closest_feasible_weight_values);

		}

	}
}

// assume left_partial_solutions
// is sorted to have weight
// be non-decreasing from left to right

// assume right_partial_solutions
// is sorted to have weight
// be non-decreasing from left to right

shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>> ListDecomposition::
	getABestPair(shared_ptr<list<shared_ptr<P>>> left_partial_solutions,
		shared_ptr<list<shared_ptr<P>>> right_partial_solutions, int capacity,
		shared_ptr<NonCoreSackSubproblem> non_core_subproblem,
		shared_ptr<PostListDecomposeSubproblem> left_problem,
		shared_ptr<PostListDecomposeSubproblem> right_problem) {

	// get best score values for particular max. weight
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> left_max_score_values =
			ListDecomposition::
			getMaxScoreValuesGivenMaxWeight(left_partial_solutions, non_core_subproblem);
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> right_max_score_values =
			ListDecomposition::
			getMaxScoreValuesGivenMaxWeight(right_partial_solutions, non_core_subproblem);
	// get residual capacities
	shared_ptr<list<shared_ptr<int>>> residual_capacities = ListDecomposition::
			getResidualCapacitiesGivenPartialSolutions(left_partial_solutions, capacity);
	// get weight values
	shared_ptr<list<shared_ptr<int>>> weight_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	weight_values->resize(right_partial_solutions->size(), NULL);
	transform(right_partial_solutions->begin(), right_partial_solutions->end(),
			weight_values->begin(),
			[&] (shared_ptr<P> a) { return shared_ptr<int>(new int(a->getTotalWeight())); });
	// prepare weight values for linear-time comparison
	shared_ptr<list<shared_ptr<int>>> reversed_residual_capacities =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>(*residual_capacities));
	reversed_residual_capacities->reverse();
	// prepare weight values for matching against actual items
	shared_ptr<list<shared_ptr<int>>> reversed_closest_feasible_weight_values =
			ListDecomposition::
				getClosestFeasibleWeightValuesGivenResidualCapacities(reversed_residual_capacities,
						weight_values);
	shared_ptr<list<shared_ptr<int>>> closest_feasible_weight_values =
			shared_ptr<list<shared_ptr<int>>>(new
					list<shared_ptr<int>>(*reversed_closest_feasible_weight_values));
	closest_feasible_weight_values->reverse();
	// prepare actual items for retrieval of max. profit
	shared_ptr<unordered_map<int, shared_ptr<tuple<shared_ptr<longlong>,
		shared_ptr<A>>>>> right_max_weight_to_score_dict =
				shared_ptr<unordered_map<int, shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>(new
					unordered_map<int, shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>());
	// new unordered_map<int, tuple<longlong *, A *> *>(5);
	// for dealing with a bug relating to empty map
	// right_max_weight_to_score_dict->insert(*(new pair<int, tuple<longlong *, A *> *>(-1, NULL)));
	auto iterator1 = right_partial_solutions->begin();
	auto iterator2 = right_max_score_values->begin();
	while (iterator1 != right_partial_solutions->end()) {
		// cout << "iterating" << endl;
		shared_ptr<P> curr_right_partial_solution = *iterator1;
		int curr_max_weight = curr_right_partial_solution->getTotalWeight();
		shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> curr_max_score = *iterator2;
		shared_ptr<pair<int, shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> curr_pair =
				shared_ptr<pair<int, shared_ptr<tuple<shared_ptr<longlong>,
				shared_ptr<A>>>>>(new pair<int, shared_ptr<tuple<shared_ptr<longlong>,
						shared_ptr<A>>>>(curr_max_weight, curr_max_score));
		// cout << "curr. max. weight: " + to_string(curr_max_weight) << endl;
		auto result_iter = right_max_weight_to_score_dict->find(curr_max_weight);
		if (result_iter != right_max_weight_to_score_dict->end()) {
			// cout << "did find a match" << endl;
			right_max_weight_to_score_dict->erase(result_iter);
		}
		// cout << get<0>(*curr_pair) << endl;
		right_max_weight_to_score_dict->insert(*curr_pair);
		advance(iterator1, 1);
		advance(iterator2, 1);
	}
	// prepare max. contribution for arbitrary q value
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> right_max_score_value_contributions =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>());
	right_max_score_value_contributions->
		resize(closest_feasible_weight_values->size(), NULL);
	transform(closest_feasible_weight_values->begin(),
			closest_feasible_weight_values->end(),
			right_max_score_value_contributions->begin(),
			[&] (shared_ptr<int> a)
			{ return right_max_weight_to_score_dict->find(*a)->second; });

	/*
	[&] (int *a) { cout << *a << endl;
	return right_max_weight_to_score_dict->find(*a)->second; });
	*/

	// if (right_max_weight_to_score_dict->find(*a) == right_max_weight_to_score_dict->end()) throw "error";

	// choose a p value
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> left_max_score_value_contributions =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>());
	left_max_score_value_contributions->
		resize(left_partial_solutions->size(), NULL);
	transform(left_partial_solutions->begin(),
			left_partial_solutions->end(),
			left_max_score_value_contributions->begin(),
			[&] (shared_ptr<P> a)
			{ return shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>(new tuple<shared_ptr<longlong>,
					shared_ptr<A>>(shared_ptr<longlong>(new longlong(a->getTotalProfit())),
					(a->toPartialSolutionPathLabel()))); });
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>
		max_combined_score_for_p_and_arbitrary_q =
				shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>());
	auto next_left_iterator = left_max_score_value_contributions->begin();
	auto next_right_iterator = right_max_score_value_contributions->begin();
	while(next_left_iterator != left_max_score_value_contributions->end()) {
		shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> curr_left_contribution =
				*next_left_iterator;
		shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> curr_right_contribution =
				*next_right_iterator;
		shared_ptr<longlong> left_profit;
		shared_ptr<A> left_path_label;
		tie(left_profit, left_path_label) = *curr_left_contribution;
		shared_ptr<longlong> right_profit;
		shared_ptr<A> right_path_label;
		tie(right_profit, right_path_label) = *curr_right_contribution;
		shared_ptr<SackItem> split_sack_item =
				non_core_subproblem->_getSplitSackItem();
		shared_ptr<BreakPartialSolution> break_partial_solution =
				non_core_subproblem->_getBreakPartialSolution();
		shared_ptr<A> combined_path_label = PartialSolutionPathLabel::
				_combinePathLabels(left_path_label, right_path_label,
						split_sack_item, break_partial_solution,
						left_problem, right_problem);
		longlong total_profit = *left_profit + *right_profit;
		shared_ptr<longlong> next_total_profit = shared_ptr<longlong>(new longlong(total_profit));
		shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> curr_score =
				shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>(new
						tuple<shared_ptr<longlong>, shared_ptr<A>>(next_total_profit,
								combined_path_label));
		max_combined_score_for_p_and_arbitrary_q->push_back(curr_score);
		advance(next_left_iterator, 1);
		advance(next_right_iterator, 1);
	}
	shared_ptr<list<shared_ptr<longlong>>> profit_values =
			shared_ptr<list<shared_ptr<longlong>>>(new list<shared_ptr<longlong>>());
	profit_values->resize(max_combined_score_for_p_and_arbitrary_q->size(), NULL);
	transform(max_combined_score_for_p_and_arbitrary_q->begin(),
			max_combined_score_for_p_and_arbitrary_q->end(),
			profit_values->begin(),
			[&] (shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> a)
			{ return get<0>(*a); });
	shared_ptr<longlong> max_max_score_combined_profit =
			accumulate(profit_values->begin(), profit_values->end(),
					shared_ptr<longlong>(new longlong(0)),
					[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
					{ return (*a > *b) ? a : b; });
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>> best_profit_profit_path_label_pairs =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>>>(*max_combined_score_for_p_and_arbitrary_q));
	best_profit_profit_path_label_pairs->
		erase(remove_if(best_profit_profit_path_label_pairs->begin(),
			best_profit_profit_path_label_pairs->end(),
			[&] (shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> a)
			{ return (*(get<0>(*a)) == *max_max_score_combined_profit) == false; }),
				best_profit_profit_path_label_pairs->end());
	shared_ptr<list<shared_ptr<A>>> best_profit_path_labels =
			shared_ptr<list<shared_ptr<A>>>(new list<shared_ptr<A>>());
	best_profit_path_labels->resize(best_profit_profit_path_label_pairs->size(), NULL);
	transform(best_profit_profit_path_label_pairs->begin(),
			best_profit_profit_path_label_pairs->end(),
			best_profit_path_labels->begin(),
			[&] (shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> a)
			{ return get<1>(*a); });
	shared_ptr<A> max_max_score_combined_path_label =
			PartialSolutionPathLabel::getMin(best_profit_path_labels);
	shared_ptr<list<shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>>>
		candidate_p_items_tagged_with_closest_feasible_weight_value =
				shared_ptr<list<shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>>());
	auto next_iterator1 = max_combined_score_for_p_and_arbitrary_q->begin();
	auto next_iterator2 = left_partial_solutions->begin();
	auto next_iterator3 = closest_feasible_weight_values->begin();
	while(next_iterator2 != left_partial_solutions->end()) {
		shared_ptr<tuple<shared_ptr<longlong>, shared_ptr<A>>> curr_max_combined_score = *next_iterator1;
		shared_ptr<P> curr_p_item = *next_iterator2;
		shared_ptr<int> closest_feasible_weight_value = *next_iterator3;
		shared_ptr<longlong> curr_max_score_combined_profit;
		shared_ptr<A> curr_max_score_combined_path_label;
		tie(curr_max_score_combined_profit,
				curr_max_score_combined_path_label) =
						*curr_max_combined_score;
		// we are content with a single match as we
		// know that identifier-based lexicographic ordering
		// leads to unambiguous best profit-path-label pair;
		// if we were not, we could use path-label equality test
		// rather than a pointer test
		if ((*curr_max_score_combined_profit ==
				*max_max_score_combined_profit) &&
				(curr_max_score_combined_path_label->
						isEqualTo(max_max_score_combined_path_label))) {
			shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> curr_pair =
					shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>(new
							tuple<shared_ptr<P>, shared_ptr<int>>(curr_p_item,
							closest_feasible_weight_value));
			candidate_p_items_tagged_with_closest_feasible_weight_value->
				push_back(curr_pair);
		}
		advance(next_iterator1, 1);
		advance(next_iterator2, 1);
		advance(next_iterator3, 1);
	}
	// had a bug here; dealt with not providing a starting object
	// for purpose of making a shared pointer
	shared_ptr<list<shared_ptr<P>>> candidate_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	candidate_partial_solutions->
		resize(candidate_p_items_tagged_with_closest_feasible_weight_value->size(),
			NULL);
	transform(candidate_p_items_tagged_with_closest_feasible_weight_value->begin(),
			candidate_p_items_tagged_with_closest_feasible_weight_value->end(),
					candidate_partial_solutions->begin(),
					[&] (shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> a)
					{ return get<0>(*a); });
	shared_ptr<list<shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>>> tagged_candidate_partial_solutions =
			candidate_p_items_tagged_with_closest_feasible_weight_value;
	shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> chosen_p_item_tagged_with_closest_feasible_weight_value =
			tagged_candidate_partial_solutions->front();
	shared_ptr<P> chosen_p_item;
	shared_ptr<int> closest_feasible_weight_value_for_chosen_p_item;
	tie(chosen_p_item, closest_feasible_weight_value_for_chosen_p_item) =
			*chosen_p_item_tagged_with_closest_feasible_weight_value;
	// choose a q item
	longlong right_max_profit_value_contribution =
			*max_max_score_combined_profit - chosen_p_item->getTotalProfit();
	shared_ptr<list<shared_ptr<P>>> candidate_q_items =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	auto next_next_iterator = right_partial_solutions->begin();
	while (next_next_iterator != right_partial_solutions->end()) {
		shared_ptr<P> curr_q_item = *next_next_iterator;
		longlong curr_profit = curr_q_item->getTotalProfit();
		int curr_weight = curr_q_item->getTotalWeight();
		shared_ptr<P> left_partial_solution = chosen_p_item;
		shared_ptr<P> right_partial_solution = curr_q_item;
		shared_ptr<A> left_path_label =
				left_partial_solution->toPartialSolutionPathLabel();
		shared_ptr<A> right_path_label =
				right_partial_solution->toPartialSolutionPathLabel();
		shared_ptr<SackItem> split_sack_item =
				non_core_subproblem->_getSplitSackItem();
		shared_ptr<BreakPartialSolution> break_partial_solution =
				non_core_subproblem->_getBreakPartialSolution();
		shared_ptr<A> combined_path_label = PartialSolutionPathLabel::
			_combinePathLabels(left_path_label, right_path_label,
				split_sack_item, break_partial_solution,
				left_problem, right_problem);
		if ((curr_profit == right_max_profit_value_contribution) &&
				(curr_weight <= *closest_feasible_weight_value_for_chosen_p_item) &&
				(combined_path_label->isEqualTo(max_max_score_combined_path_label))) {
			candidate_q_items->push_back(curr_q_item);
		}
		advance(next_next_iterator, 1);
	}
	// cout << "# of q items: " + to_string(candidate_q_items->size()) << endl;
	shared_ptr<list<shared_ptr<P>>> next_candidate_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*candidate_q_items));
	shared_ptr<list<shared_ptr<P>>> next_next_candidate_partial_solutions = next_candidate_partial_solutions;
	shared_ptr<P> chosen_q_item =
			next_next_candidate_partial_solutions->front();
	// have a pair
	shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>> chosen_pair =
			shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>>(new
					tuple<shared_ptr<P>, shared_ptr<P>>(chosen_p_item, chosen_q_item));
	return chosen_pair;
}

// #include "FractionalKnapsack.hpp"

void FractionalKnapsack::ponder(int n) {
	shared_ptr<list<shared_ptr<longdouble>>> l1 =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	l1->push_back(shared_ptr<longdouble>(new longdouble(1)));
	l1->push_back(shared_ptr<longdouble>(new longdouble(2)));
	l1->push_back(shared_ptr<longdouble>(new longdouble(3)));

	shared_ptr<longdouble> num = FractionalKnapsack::quickSelect(l1, 1);

	cout << *num << endl;

	shared_ptr<list<shared_ptr<longdouble>>> item_collection =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>(*l1));

	shared_ptr<longdouble> median = FractionalKnapsack::getMedian(item_collection);

	cout << *median << endl;

	shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> weighted_items =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>());

weighted_items->push_back(shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>(new
		tuple<shared_ptr<longdouble>, shared_ptr<int>>(shared_ptr<longdouble>(new longdouble(1)),
		shared_ptr<int>(new int(3)))));
weighted_items->push_back(shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>(new
		tuple<shared_ptr<longdouble>, shared_ptr<int>>(shared_ptr<longdouble>(new longdouble(2)),
		shared_ptr<int>(new int(4)))));
weighted_items->push_back(shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>(new
		tuple<shared_ptr<longdouble>, shared_ptr<int>>(shared_ptr<longdouble>(new longdouble(3)),
		shared_ptr<int>(new int(5)))));

int W = 5;

shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> weighted_median =
		FractionalKnapsack::getWeightedMedian(weighted_items, W);

shared_ptr<longdouble> z;

shared_ptr<int> w;

tie(z, w) = *weighted_median;

cout << to_string(*z) << endl;

cout << to_string(*w) << endl;

shared_ptr<list<shared_ptr<tuple<int, int, int>>>> items =
		shared_ptr<list<shared_ptr<tuple<int, int, int>>>>(new
				list<shared_ptr<tuple<int, int, int>>>());

items->push_back(shared_ptr<tuple<int, int, int>>(new tuple<int, int, int>(50, 30, 1)));
items->push_back(shared_ptr<tuple<int, int, int>>(new tuple<int, int, int>(40, 20, 2)));
items->push_back(shared_ptr<tuple<int, int, int>>(new tuple<int, int, int>(45, 40, 3)));
items->push_back(shared_ptr<tuple<int, int, int>>(new tuple<int, int, int>(45, 20, 4)));

shared_ptr<list<shared_ptr<SackItem>>> sack_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());

sack_items->resize(items->size(), NULL);

transform(items->begin(), items->end(), sack_items->begin(),
		[&] (shared_ptr<tuple<int, int, int>> a)
		{ return shared_ptr<SackItem>(new SackItem(get<0>(*a), get<1>(*a), get<2>(*a))); });

int capacity = 100;

shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>, shared_ptr<SackItem>,
	shared_ptr<longdouble>>> result =
		FractionalKnapsack::linearTimeFractionalSolve(sack_items, capacity);

shared_ptr<list<shared_ptr<SackItem>>> chosen_items;
shared_ptr<SackItem> split_item;
shared_ptr<longdouble> amount_of_split_item;

tie(chosen_items, split_item, amount_of_split_item) = *result;

shared_ptr<list<shared_ptr<string>>> chosen_item_str_list =
		shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());

chosen_item_str_list->resize(chosen_items->size(), NULL);

transform(chosen_items->begin(), chosen_items->end(),
		chosen_item_str_list->begin(),
		[&] (shared_ptr<SackItem> a) { return a->toString(); });

shared_ptr<string> chosen_item_str = accumulate(chosen_item_str_list->begin(),
		chosen_item_str_list->end(), shared_ptr<string>(new string("")),
		[&] (shared_ptr<string> a, shared_ptr<string> b)
		{ return shared_ptr<string>(new string(*a + " " + *b)); });

cout << *chosen_item_str << endl;
cout << *(split_item->toString()) << endl;
cout << *amount_of_split_item << endl;

}



shared_ptr<longdouble> FractionalKnapsack::quickSelect(shared_ptr<list<shared_ptr<longdouble>>> S, int k) {
	if (S->size() == 0) {
		return NULL;
	} else if (S->size() == 1) {
		return S->front();
	} else {
		int pivot_index = (int) abs((long int) rand() % (long int) S->size());
		auto iterator = S->begin();
		advance(iterator, pivot_index - 1 + 1);
		shared_ptr<longdouble> pivot = *iterator;
		longdouble next_pivot = *pivot;
		// cout << next_pivot << endl;
		shared_ptr<list<shared_ptr<longdouble>>> L =
				shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>(*S));
		shared_ptr<list<shared_ptr<longdouble>>> E =
				shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>(*S));
		shared_ptr<list<shared_ptr<longdouble>>> G =
				shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>(*S));
		L->erase(remove_if(L->begin(), L->end(),
				[&] (shared_ptr<longdouble> a)
				{ return (*a < next_pivot) == false; }), L->end());
		// cout << "compared values: " << *a << " " << next_pivot << endl;
		E->erase(remove_if(E->begin(), E->end(),
				[&] (shared_ptr<longdouble> a) { return (*a == next_pivot) == false; }), E->end());
		G->erase(remove_if(G->begin(), G->end(),
				[&] (shared_ptr<longdouble> a) { return (*a > next_pivot) == false; }), G->end());
		// cout << L->size() << " "<< E->size() << " " << G->size() << endl;
		if (k <= ((int) L->size())) {
			return FractionalKnapsack::quickSelect(L, k);
		} else if (k <= ((int) (L->size() + E->size()))) {
			return pivot;
		} else {
			return FractionalKnapsack::quickSelect(G, k - L->size() - E->size());
		}

	}
}

shared_ptr<longdouble> FractionalKnapsack::getMedian(shared_ptr<list<shared_ptr<longdouble>>> items) {
	shared_ptr<list<shared_ptr<longdouble>>> S =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>(*items));
	int num_items = items->size();
	int k;
	if (num_items % 2 == 0) {
		k = num_items / 2;
	} else {
		// num_items % 2 == 1
		k = (num_items - 1) / 2 + 1;
	}
	return FractionalKnapsack::quickSelect(S, k);
}

// items are (z, w) two-tuples

shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>
	FractionalKnapsack::
		getWeightedMedian(shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>,
				shared_ptr<int>>>>> items, int W) {

	if(items->size() == 0) {
		return NULL;
	}
	shared_ptr<list<shared_ptr<longdouble>>> z_values =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	z_values->resize(items->size(), NULL);
	transform(items->begin(), items->end(), z_values->begin(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a) { return get<0>(*a); });
	shared_ptr<longdouble> median_z_value = FractionalKnapsack::getMedian(z_values);
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> candidate_median_items =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>(*items));
	remove_if(candidate_median_items->begin(), candidate_median_items->end(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return (*(get<0>(*a)) == *median_z_value) == false; });
	shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> median_item =
			candidate_median_items->front();
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> L_items =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>(*items));
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> E_items =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>(*items));
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> G_items =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>(*items));
	L_items->erase(remove_if(L_items->begin(), L_items->end(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return (*(get<0>(*a)) < *median_z_value) == false; }), L_items->end());
	E_items->erase(remove_if(E_items->begin(), E_items->end(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return (*(get<0>(*a)) == *median_z_value) == false; }), E_items->end());
	G_items->erase(remove_if(G_items->begin(), G_items->end(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return (*(get<0>(*a)) > *median_z_value) == false; }), G_items->end());
	shared_ptr<list<shared_ptr<int>>> L_weights =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	L_weights->resize(L_items->size(), NULL);
	transform(L_items->begin(), L_items->end(), L_weights->begin(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return get<1>(*a); });
	shared_ptr<list<shared_ptr<int>>> E_weights =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	E_weights->resize(E_items->size(), NULL);
	transform(E_items->begin(), E_items->end(), E_weights->begin(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return get<1>(*a); });
	shared_ptr<list<shared_ptr<int>>> G_weights =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	G_weights->resize(G_items->size(), NULL);
	transform(G_items->begin(), G_items->end(), G_weights->begin(),
			[&] (shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> a)
			{ return get<1>(*a); });
	shared_ptr<int> L_sum = accumulate(L_weights->begin(), L_weights->end(), shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	shared_ptr<int> E_sum = accumulate(E_weights->begin(), E_weights->end(), shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	shared_ptr<int> G_sum = accumulate(G_weights->begin(), G_weights->end(), shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	int next_L_sum = *L_sum;
	int next_E_sum = *E_sum;
	int next_G_sum = *G_sum;

	if ((next_L_sum < W) && (W <= (next_L_sum + next_E_sum))) {
		return median_item;
	} else if ((next_L_sum + next_E_sum) < W) {
		return FractionalKnapsack::getWeightedMedian(G_items,
				W - (next_L_sum + next_E_sum));
	} else {
		// L_sum >= W
		return FractionalKnapsack::getWeightedMedian(L_items, W);
	}

}

shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>, shared_ptr<SackItem>, shared_ptr<longdouble>>>
	FractionalKnapsack::linearTimeFractionalSolve(shared_ptr<list<shared_ptr<SackItem>>> items,
		int capacity) {
	if (items->size() == 0) {
		shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
			shared_ptr<SackItem>, shared_ptr<longdouble>>> result =
					shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
				shared_ptr<SackItem>, shared_ptr<longdouble>>>(new tuple<shared_ptr<list<shared_ptr<SackItem>>>,
				shared_ptr<SackItem>, shared_ptr<longdouble>>(shared_ptr<list<shared_ptr<SackItem>>>(new
						list<shared_ptr<SackItem>>()),
						shared_ptr<SackItem>(NULL), shared_ptr<longdouble>(NULL)));
		return result;
	}
	shared_ptr<list<shared_ptr<int>>> weights =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	weights->resize(items->size(), NULL);
	transform(items->begin(), items->end(), weights->begin(),
			[&] (shared_ptr<SackItem> a) { return shared_ptr<int>(new int(a->getWeight())); });
	shared_ptr<int> weight_sum = accumulate(weights->begin(), weights->end(), shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	int next_weight_sum = *weight_sum;
	if (next_weight_sum <= capacity) {
		shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
			shared_ptr<SackItem>, shared_ptr<longdouble>>> result =
					shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
				shared_ptr<SackItem>, shared_ptr<longdouble>>>(new
						tuple<shared_ptr<list<shared_ptr<SackItem>>>,
				shared_ptr<SackItem>, shared_ptr<longdouble>>(items,
						shared_ptr<SackItem>(NULL), shared_ptr<longdouble>(NULL)));
		return result;
	}
	shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>> z_w_pairs =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>>(new
					list<shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>>());
	z_w_pairs->resize(items->size(), NULL);
	transform(items->begin(), items->end(), z_w_pairs->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>>(new
					tuple<shared_ptr<longdouble>, shared_ptr<int>>(shared_ptr<longdouble>(new
							longdouble(-1 * a->getProfitWeightRatio())),
							make_shared<int>(*(new int(a->getWeight()))))); });
	shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<int>>> weighted_median_z_w_pair =
			getWeightedMedian(z_w_pairs, capacity);
	shared_ptr<longdouble> z;
	shared_ptr<int> w;
	tie(z, w) = *weighted_median_z_w_pair;
	shared_ptr<list<shared_ptr<SackItem>>> candidate_weighted_median_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*items));
	// could be asking for trouble here
	candidate_weighted_median_items->
		erase(remove_if(candidate_weighted_median_items->begin(),
				candidate_weighted_median_items->end(),
				[&] (shared_ptr<SackItem> a)
				{ longdouble difference = abs(a->getProfitWeightRatio() - (-1 * *z));
				// cout << "difference: " << difference << endl;
				return (difference <= 0.00001) == false; }),
				candidate_weighted_median_items->end());
	shared_ptr<SackItem> chosen_weighted_median_item =
			candidate_weighted_median_items->front();
	// cout << candidate_weighted_median_items->size() << endl;
	shared_ptr<SackItem> split_item = chosen_weighted_median_item;
	longdouble split_item_ratio = split_item->getProfitWeightRatio();
	shared_ptr<list<shared_ptr<SackItem>>> G_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*items));
	shared_ptr<list<shared_ptr<SackItem>>> E_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*items));
	G_items->erase(remove_if(G_items->begin(), G_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ return (a->getProfitWeightRatio()
					> split_item_ratio) == false; }), G_items->end());
	E_items->erase(remove_if(E_items->begin(), E_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ return (a->getProfitWeightRatio()
					== split_item_ratio) == false; }), E_items->end());
	shared_ptr<list<shared_ptr<int>>> G_weights =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	G_weights->resize(G_items->size(), NULL);
	transform(G_items->begin(), G_items->end(), G_weights->begin(),
			[&] (shared_ptr<SackItem> a) { return shared_ptr<int>(new int(a->getWeight())); });
	shared_ptr<int> G_sum = accumulate(G_weights->begin(), G_weights->end(), shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	int next_G_sum = *G_sum;
	shared_ptr<list<shared_ptr<SackItem>>> chosen_items = G_items;
	longdouble amount_of_split_item =
			((longdouble) capacity - (longdouble) next_G_sum) / ((longdouble) split_item->getWeight());
	shared_ptr<longdouble> next_amount_of_split_item =
			shared_ptr<longdouble>(new longdouble(amount_of_split_item));
	shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
		shared_ptr<SackItem>, shared_ptr<longdouble>>> result =
			shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
			shared_ptr<SackItem>, shared_ptr<longdouble>>>(new
					tuple<shared_ptr<list<shared_ptr<SackItem>>>, shared_ptr<SackItem>,
			shared_ptr<longdouble>>(chosen_items, split_item, next_amount_of_split_item));
	return result;
}

shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<longdouble>>>
	FractionalKnapsack::
		toFractionalSolutionProfitAndWeightTuple(shared_ptr<PartialSolution> partial_solution,
			shared_ptr<SackItem> split_item, longdouble split_item_fraction) {
	longlong profit = partial_solution->getTotalProfit();
	int weight = partial_solution->getTotalWeight();
	longlong split_item_profit = split_item->getProfit();
	int split_item_weight = split_item->getWeight();
	longdouble total_profit =
			(longdouble) profit + (longdouble) split_item_profit * split_item_fraction;
	longdouble total_weight =
			(longdouble) weight + (longdouble) split_item_weight * split_item_fraction;
	shared_ptr<longdouble> next_total_profit = shared_ptr<longdouble>(new longdouble(total_profit));
	shared_ptr<longdouble> next_total_weight = shared_ptr<longdouble>(new longdouble(total_weight));
	shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<longdouble>>> result =
			shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<longdouble>>>(new tuple<shared_ptr<longdouble>,
					shared_ptr<longdouble>>(next_total_profit, next_total_weight));
	return result;
}

// #include "IntegralityGapEstimate.hpp"

// #include "PartialSolution.hpp"

longdouble IntegralityGapEstimate::getOptimalFractionalSolutionProfit() {
	return this->optimal_fractional_solution_profit;
}

longlong IntegralityGapEstimate::getBestIntegerSolutionProfit() {
	return this->best_integer_solution_profit;
}

void IntegralityGapEstimate::setBestIntegerSolutionProfit(longlong profit_value) {
	this->best_integer_solution_profit = profit_value;
}

longdouble IntegralityGapEstimate::getValue() {
	longdouble optimal_fractional_solution_profit =
			this->getOptimalFractionalSolutionProfit();
	longdouble best_integer_solution_profit =
			this->getBestIntegerSolutionProfit();
	longdouble difference =
			optimal_fractional_solution_profit - best_integer_solution_profit;
	return difference;
}

void IntegralityGapEstimate::updateBestIntegerSolutionProfit(longlong integer_solution_profit) {
	longlong previous_value = this->getBestIntegerSolutionProfit();
	shared_ptr<list<longlong>> candidate_values = shared_ptr<list<longlong>>(new list<longlong>());
	candidate_values->push_back(previous_value);
	candidate_values->push_back(integer_solution_profit);
	longlong max_value = accumulate(candidate_values->begin(), candidate_values->end(), 0,
			[&] (longlong a, longlong b) { return (a > b) ? a : b; });
	longlong next_value = max_value;
	this->setBestIntegerSolutionProfit(next_value);
}

IntegralityGapEstimate::IntegralityGapEstimate(longdouble optimal_fractional_solution_profit,
		longlong best_integer_solution_profit) {
	this->optimal_fractional_solution_profit = optimal_fractional_solution_profit;
	this->best_integer_solution_profit = best_integer_solution_profit;
}

IntegralityGapEstimate::~IntegralityGapEstimate() {
}

// #include "Solution.t.hpp"

int Event::getTime() {
	return this->time;
}

void Event::handle(shared_ptr<Dictionary<int, FeedItem>> item_collection) {
	return;
}

shared_ptr<string> Event::toString() {
	return NULL;
}

bool Event::isSolveEvent() {
	return false;
}

Event::Event(int time) {
	this->time = time;
}

Event::~Event() {
	return;
}

// #include "ItemEvent.hpp"

shared_ptr<FeedItem> ItemEvent::getItem() {
	return this->item;
}

ItemEvent::ItemEvent(int time, shared_ptr<FeedItem> item) : Event(time) {
	this->item = item;
}

ItemEvent::~ItemEvent() {
	(this->item).reset();
}

// #include "ItemExpireEvent.hpp"

using namespace std;

shared_ptr<string> ItemExpireEvent::toString() {
	shared_ptr<FeedItem> item = this->getItem();
	int id_value = item->getIDValue();
	shared_ptr<list<shared_ptr<string>>> component_str_values =
			shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());
	component_str_values->push_back(shared_ptr<string>(item->toString()));
	component_str_values->push_back(shared_ptr<string>(new string(to_string(id_value))));
	shared_ptr<string> combined_str = accumulate(component_str_values->begin(),
			component_str_values->end(), shared_ptr<string>(new string("")),
			[&] (shared_ptr<string> a, shared_ptr<string> b)
			{ return shared_ptr<string>(new string(*a + " " + *b)); });
	string result_str = "item expire event: " + *combined_str;
	shared_ptr<string> next_result_str = shared_ptr<string>(new string(result_str));
	return next_result_str;
}

void ItemExpireEvent::handle(shared_ptr<Dictionary<int, FeedItem>> item_collection) {
	shared_ptr<FeedItem> item = this->getItem();
	int id_value = item->getIDValue();
	shared_ptr<int> next_id_value = shared_ptr<int>(new int(id_value));
	shared_ptr<tuple<shared_ptr<int>, shared_ptr<FeedItem>>> remove_tuple =
			shared_ptr<tuple<shared_ptr<int>, shared_ptr<FeedItem>>>(new tuple<shared_ptr<int>,
					shared_ptr<FeedItem>>(next_id_value, item));
	item_collection->remove(remove_tuple);
}

ItemExpireEvent::ItemExpireEvent(int time, shared_ptr<FeedItem> item) : ItemEvent(time, item) {
	return;
}

ItemExpireEvent::~ItemExpireEvent() {
	return;
}

// #include "ItemIntroduceEvent.hpp"

shared_ptr<string> ItemIntroduceEvent::toString() {
	shared_ptr<FeedItem> item = this->getItem();
	int id_value = item->getIDValue();
	shared_ptr<list<shared_ptr<string>>> component_str_values =
			shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());
	component_str_values->push_back(item->toString());
	component_str_values->push_back(shared_ptr<string>(new string(to_string(id_value))));
	shared_ptr<string> combined_str = accumulate(component_str_values->begin(),
			component_str_values->end(), shared_ptr<string>(new string("")),
			[&] (shared_ptr<string> a, shared_ptr<string> b)
			{ return shared_ptr<string>(new string(*a + " " + *b)); });
			/*
			{ shared_ptr<string> result = make_shared<string>(*(new string("")));
			result->append(**a); result->append(string(" ")); result->append(**b);
			return result; }));
			*/
	string result_str = "item introduce event: " + *combined_str;
	// string result_str = "item introduce event: ";
	shared_ptr<string> next_result_str = shared_ptr<string>(new string(result_str));
	return next_result_str;

}
void ItemIntroduceEvent::handle(shared_ptr<Dictionary<int, FeedItem>> item_collection) {
	shared_ptr<FeedItem> item = this->getItem();
	int id_value = item->getIDValue();
	shared_ptr<int> next_id_value = shared_ptr<int>(new int(id_value));
	item_collection->insert(next_id_value, item);

}
ItemIntroduceEvent::ItemIntroduceEvent(int time, shared_ptr<FeedItem> item)
	: ItemEvent(time, item) {
	return;
}
ItemIntroduceEvent::~ItemIntroduceEvent() {
	return;
}

// #include "ItemTimeSpanningEvent.hpp"

class FeedItem;

shared_ptr<string> ItemTimeSpanningEvent::toString() {
	shared_ptr<FeedItem> item = this->getItem();
	int time = this->getTime();
	longlong profit = item->getProfit();
	int weight = item->getWeight();
	int id_value = item->getIDValue();
	shared_ptr<list<shared_ptr<string>>> component_str_values =
			shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());
	component_str_values->push_back(shared_ptr<string>(new string(to_string(time))));
	component_str_values->push_back(shared_ptr<string>(new string(to_string(profit))));
	component_str_values->push_back(shared_ptr<string>(new string(to_string(weight))));
	component_str_values->push_back(shared_ptr<string>(new string(to_string(id_value))));
	shared_ptr<string> combined_str = accumulate(component_str_values->begin(),
			component_str_values->end(), shared_ptr<string>(new string("")),
			[&] (shared_ptr<string> a, shared_ptr<string> b)
			{ return shared_ptr<string>(new string(*a + " " + *b)); });
	string result_str = "item time-spanning event: " + *combined_str;
	shared_ptr<string> next_result_str = shared_ptr<string>(new string(result_str));
	return next_result_str;
}

void ItemTimeSpanningEvent::handle(shared_ptr<Dictionary<int, FeedItem>> item_collection) {
	return;
}

ItemTimeSpanningEvent::ItemTimeSpanningEvent(int time, shared_ptr<FeedItem> item)
	: ItemEvent(time, item) {
	return;
}

ItemTimeSpanningEvent::~ItemTimeSpanningEvent() {
	return;
}

// #include "SolveEvent.hpp"

class FeedProblem;

class FeedOptimizer;

int SolveEvent::_getSackCapacity() {
	return this->sack_capacity;
}

shared_ptr<string> SolveEvent::toString() {
	int time = this->getTime();
	shared_ptr<list<shared_ptr<string>>> component_str_values =
			shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());
	component_str_values->push_back(shared_ptr<string>(new string(to_string(time))));
	shared_ptr<string> combined_str = accumulate(component_str_values->begin(),
			component_str_values->end(), shared_ptr<string>(new string("")),
			[&] (shared_ptr<string> a, shared_ptr<string> b)
			{ return shared_ptr<string>(new string(*a + " " + *b)); });
	shared_ptr<string> result_str =
			shared_ptr<string>(new string("solve event: " + *combined_str));
	return result_str;
}

/*

struct {

	bool comp(const FeedItem *&a, const FeedItem *&b) {
		return a->getIDValue() < b->getIDValue();
	}
	bool equiv(const FeedItem *&a, const FeedItem *&b) {
		return !comp(a, b) && !comp(b, a);

	bool operator()(const FeedItem *&a, const FeedItem *&b) {
		return a->getIDValue() < b->getIDValue();
	}

	bool operator-(const FeedItem *&a, const FeedItem *&b) {
		return a->getIDValue() - b->getIDValue();
	}

} feedItemComp;

*/

bool feedItemComp(shared_ptr<FeedItem> a, shared_ptr<FeedItem> b) {
	return a->getIDValue() < b->getIDValue();
}

void SolveEvent::handle(shared_ptr<Dictionary<int, FeedItem>> item_collection) {
	shared_ptr<list<shared_ptr<tuple<shared_ptr<int>,
		shared_ptr<FeedItem>>>>> entries = item_collection->entries();
	shared_ptr<list<shared_ptr<FeedItem>>> items =
			shared_ptr<list<shared_ptr<FeedItem>>>(new list<shared_ptr<FeedItem>>());
	items->resize(entries->size(), NULL);
	transform(entries->begin(), entries->end(),
			items->begin(),
			[&] (shared_ptr<tuple<shared_ptr<int>, shared_ptr<FeedItem>>> a)
			{ return get<1>(*a); });
	int sack_capacity = this->_getSackCapacity();
	shared_ptr<FeedProblem> problem = shared_ptr<FeedProblem>(new FeedProblem(items, sack_capacity));
	shared_ptr<FeedProblem> next_problem = FeedOptimizer::transformForMinimizingSolutionSize(problem);
	shared_ptr<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>, shared_ptr<longlong>>> result =
			next_problem->solve();
	shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>> item_list_list;
	shared_ptr<longlong> total_profit;
	tie(item_list_list, total_profit) = *result;
	// cout << "total profit: " << to_string(*total_profit) << endl;
	shared_ptr<list<shared_ptr<FeedItem>>> item_list = item_list_list->front();
	shared_ptr<tuple<shared_ptr<list<shared_ptr<FeedItem>>>, shared_ptr<longlong>>> next_result =
			FeedOptimizer::untransformForMinimizingSolutionSize(problem,
					next_problem, item_list, *total_profit);

	shared_ptr<list<shared_ptr<FeedItem>>> next_item_list;
	shared_ptr<longlong> next_total_profit;
	tie(next_item_list, next_total_profit) = *next_result;
	// cout << *next_total_profit << endl;
	shared_ptr<vector<shared_ptr<FeedItem>>> sorted_item_vector =
			shared_ptr<vector<shared_ptr<FeedItem>>>(new vector<shared_ptr<FeedItem>>());
	for_each(next_item_list->begin(), next_item_list->end(),
			[&] (shared_ptr<FeedItem> a) { sorted_item_vector->push_back(a); });
	// list<FeedItem *> *sorted_item_list = new list<FeedItem *>(*next_item_list);
	sort(sorted_item_vector->begin(), sorted_item_vector->end(), feedItemComp);

			/*
			[&] (FeedItem *a, FeedItem *b)
			{ return a->getIDValue() < b->getIDValue(); });
			*/
	int num_solution_items = sorted_item_vector->size();
shared_ptr<list<shared_ptr<string>>> sorted_item_list_strings =
		shared_ptr<list<shared_ptr<string>>>(new list<shared_ptr<string>>());
sorted_item_list_strings->resize(sorted_item_vector->size(), NULL);
transform(sorted_item_vector->begin(), sorted_item_vector->end(),
		sorted_item_list_strings->begin(),
		[&] (shared_ptr<FeedItem> a) { return shared_ptr<string>(new string(to_string(a->getIDValue()))); });
shared_ptr<string> joined_sorted_item_list_string = accumulate(sorted_item_list_strings->begin(),
		sorted_item_list_strings->end(), shared_ptr<string>(new string("")),
		[&] (shared_ptr<string> a, shared_ptr<string> b)
		{ return shared_ptr<string>(new string(*a + " " + *b)); });
shared_ptr<list<shared_ptr<int>>> weight_values =
		shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>);
weight_values->resize(sorted_item_vector->size(), NULL);
transform(sorted_item_vector->begin(), sorted_item_vector->end(),
		weight_values->begin(),
		[&] (shared_ptr<FeedItem> a)
		{ return shared_ptr<int>(new int(a->getWeight())); });
shared_ptr<int> total_weight =
		accumulate(weight_values->begin(), weight_values->end(),
				shared_ptr<int>(new int(0)),
		[&] (shared_ptr<int> a, shared_ptr<int> b)
		{ return shared_ptr<int>(new int(*a + *b)); });
longlong result_total_profit = *next_total_profit;
int result_total_weight = *total_weight;
if (num_solution_items == 0) {
	cout << to_string(result_total_profit) << " " << to_string(num_solution_items) << endl;
} else {
	cout << to_string(result_total_profit) << " " << to_string(num_solution_items) << *joined_sorted_item_list_string << endl;
}

}

bool SolveEvent::isSolveEvent() {
	return true;
}

SolveEvent::SolveEvent(int time, int sack_capacity) : Event(time) {
	this->sack_capacity = sack_capacity;
}

SolveEvent::~SolveEvent() {
	// cout << "destructing a solve event" << endl;
}

// #include "Dictionary.t.hpp"

shared_ptr<string> getKVPairString(shared_ptr<list<shared_ptr<tuple<shared_ptr<int>,
		shared_ptr<int>>>>> tuple_list) {

	// cout << "getting kv-pair string" << endl;

	string result_str = "";

	auto iterator = tuple_list->begin();

	// cout << "about to begin iterating" << endl;

	while (iterator != tuple_list->end()) {

		// cout << "iterating" << endl;

		shared_ptr<tuple<shared_ptr<int>, shared_ptr<int>>> curr_tuple = *iterator;

		shared_ptr<int> k;

		shared_ptr<int> v;

		tie(k, v) = *curr_tuple;

		result_str = result_str + "(" + to_string(*k) + ", " + to_string(*v) + ")" + "\n";

		advance(iterator, 1);

	}

	shared_ptr<string> result = shared_ptr<string>(new string(result_str));

	return result;

}

/*

#include "EventPriorityQueue.hpp"

#include "../feed_optimizer/FeedItem.hpp"

// #include "../feed_optimizer/events/ItemTimeSpanningEvent.hpp"

#include "../feed_optimizer/Event.hpp"

*/

/*

using Q = priority_queue<Event *, vector<Event *>,
		decltype(EventTimeAscendingComparator::_comparator)>;

*/

using Q = priority_queue<shared_ptr<Event>, vector<shared_ptr<Event>>,
		function<bool(shared_ptr<Event>, shared_ptr<Event>)>>;

void EventPriorityQueue::ponder(int n) {
	shared_ptr<FeedItem> feed_item1 = shared_ptr<FeedItem>(new FeedItem(45, 20, 1));
	shared_ptr<FeedItem> feed_item2 = shared_ptr<FeedItem>(new FeedItem(40, 20, 2));
	shared_ptr<FeedItem> feed_item3 = shared_ptr<FeedItem>(new FeedItem(45, 40, 3));
	shared_ptr<FeedItem> feed_item4 = shared_ptr<FeedItem>(new FeedItem(50, 30, 4));
	shared_ptr<ItemTimeSpanningEvent> event1 =
			shared_ptr<ItemTimeSpanningEvent>(new ItemTimeSpanningEvent(10, feed_item1));
	shared_ptr<ItemTimeSpanningEvent> event2 =
			shared_ptr<ItemTimeSpanningEvent>(new ItemTimeSpanningEvent(5, feed_item2));
	shared_ptr<ItemTimeSpanningEvent> event3 =
			shared_ptr<ItemTimeSpanningEvent>(new ItemTimeSpanningEvent(20, feed_item3));
	shared_ptr<ItemTimeSpanningEvent> event4 =
			shared_ptr<ItemTimeSpanningEvent>(new ItemTimeSpanningEvent(2, feed_item4));
	shared_ptr<EventPriorityQueue> priority_queue =
			shared_ptr<EventPriorityQueue>(new EventPriorityQueue());
	priority_queue->pushEvent(event1);
	priority_queue->pushEvent(event2);
	priority_queue->pushEvent(event3);
	priority_queue->pushEvent(event4);
	shared_ptr<Event> result = priority_queue->peek();
	shared_ptr<ItemTimeSpanningEvent> next_result =
			static_pointer_cast<ItemTimeSpanningEvent>(result);
	int time = next_result->getTime();
	shared_ptr<FeedItem> feed_item = next_result->getItem();
	int id_value = feed_item->getIDValue();
	cout << id_value << endl;
	bool is_empty = priority_queue->isEmpty();
	if (is_empty == true) {
		cout << "priority queue is empty" << endl;
	} else {
		cout << "priority queue is not empty" << endl;
	}
	shared_ptr<Event> popped_event1 = priority_queue->popEvent();
	shared_ptr<Event> popped_event2 = priority_queue->popEvent();
	shared_ptr<Event> popped_event3 = priority_queue->popEvent();
	shared_ptr<Event> popped_event4 = priority_queue->popEvent();
	shared_ptr<ItemTimeSpanningEvent> next_popped_event1 =
			static_pointer_cast<ItemTimeSpanningEvent>(popped_event1);
	shared_ptr<ItemTimeSpanningEvent> next_popped_event2 =
			static_pointer_cast<ItemTimeSpanningEvent>(popped_event2);
	shared_ptr<ItemTimeSpanningEvent> next_popped_event3 =
			static_pointer_cast<ItemTimeSpanningEvent>(popped_event3);
	shared_ptr<ItemTimeSpanningEvent> next_popped_event4 =
			static_pointer_cast<ItemTimeSpanningEvent>(popped_event4);
	shared_ptr<FeedItem> next_feed_item1 = next_popped_event1->getItem();
	shared_ptr<FeedItem> next_feed_item2 = next_popped_event2->getItem();
	shared_ptr<FeedItem> next_feed_item3 = next_popped_event3->getItem();
	shared_ptr<FeedItem> next_feed_item4 = next_popped_event4->getItem();
	int id_value1 = next_feed_item1->getIDValue();
	int id_value2 = next_feed_item2->getIDValue();
	int id_value3 = next_feed_item3->getIDValue();
	int id_value4 = next_feed_item4->getIDValue();
	cout << id_value1 << endl;
	cout << id_value2 << endl;
	cout << id_value3 << endl;
	cout << id_value4 << endl;
}

shared_ptr<Q> EventPriorityQueue::_getPriorityQueue() {
	return this->pqueue;
}

void EventPriorityQueue::pushEvent(shared_ptr<Event> event) {
	shared_ptr<Q> pqueue = this->_getPriorityQueue();
	pqueue->push(event);
}

shared_ptr<Event> EventPriorityQueue::popEvent() {
	shared_ptr<Q> pqueue = this->_getPriorityQueue();
	shared_ptr<Event> result = this->peek();
	pqueue->pop();
	return result;
}

bool EventPriorityQueue::isEmpty() {
	shared_ptr<Q> pqueue = this->_getPriorityQueue();
	bool is_empty = pqueue->size() == 0;
	return is_empty;
}

shared_ptr<Event> EventPriorityQueue::peek() {
	shared_ptr<Q> pqueue = this->_getPriorityQueue();
	shared_ptr<Event> result = pqueue->top();
	return result;
}

bool EventPriorityQueue::_comparator(shared_ptr<Event> a, shared_ptr<Event> b) {

	// time descending;
	// we retrieve element most towards
	// end for priority queue

	int time_a = a->getTime();
	int time_b = b->getTime();
	//  << to_string(time_a) << " " << to_string(time_b) << endl;
	if (time_a == time_b) {
		return false;
	} else if (time_a > time_b) {
		return true;
	} else if (time_a < time_b) {
		return false;
	}
}

EventPriorityQueue::EventPriorityQueue() {
	this->pqueue = shared_ptr<Q>(new Q(EventPriorityQueue::_comparator));
}

EventPriorityQueue::~EventPriorityQueue() {
	// cout << "destructing an event priority queue" << endl;
	(this->pqueue).reset();
}

// #include "FeedItem.hpp"

// #include "Solution.t.hpp"

longlong FeedItem::getProfit() {
	return this->profit;
}

int FeedItem::getWeight() {
	return this->weight;
}

int FeedItem::getIDValue() {
	return this->id_value;
}

shared_ptr<string> FeedItem::toString() {
	longlong profit = this->getProfit();
	int weight = this->getWeight();
	int id_value = this->getIDValue();
	string result_str = "(" + to_string(profit) + ", "
			+ to_string(weight) + ", " + to_string(id_value) + ")";
	shared_ptr<string> next_result_str = make_shared<string>(*(new string(result_str)));
	return next_result_str;
}

FeedItem::FeedItem(longlong profit, int weight, int id_value) {
	this->profit = profit;
	this->weight = weight;
	this->id_value = id_value;
}

FeedItem::~FeedItem() {
	return;
}

// #include "FeedProblem.hpp"

// #include "Solution.t.hpp"

shared_ptr<longlong> FeedProblem::_getMaxItemProfit(shared_ptr<list<shared_ptr<FeedItem>>> items) {
	if (items->size() == 0) {
		return NULL;
	} else {
		shared_ptr<list<shared_ptr<longlong>>> profit_values =
				make_shared<list<shared_ptr<longlong>>>(*(new list<shared_ptr<longlong>>()));
		profit_values->resize(items->size(), NULL);
		transform(items->begin(), items->end(),
				profit_values->begin(),
				[&] (shared_ptr<FeedItem> a)
				{ return make_shared<longlong>(*(new longlong(a->getProfit()))); });
		shared_ptr<longlong> max_profit_value = accumulate(profit_values->begin(),
				profit_values->end(), make_shared<longlong>(*(new longlong(0))),
				[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
				{ return ((*a > *b) ? make_shared<longlong>(*(new longlong(*a))) :
						make_shared<longlong>(*(new longlong(*b)))); });
		// longlong next_max_profit_value = *max_profit_value;
		// return next_max_profit_value;
		return max_profit_value;
	}
}

shared_ptr<int> FeedProblem::_getMaxItemWeight(shared_ptr<list<shared_ptr<FeedItem>>> items) {
	if (items->size() == 0) {
		return NULL;
	} else {
		shared_ptr<list<shared_ptr<int>>> weight_values =
				make_shared<list<shared_ptr<int>>>(*(new list<shared_ptr<int>>()));
		weight_values->resize(items->size(), NULL);
		transform(items->begin(), items->end(),
				weight_values->begin(),
				[&] (shared_ptr<FeedItem> a)
				{ return make_shared<int>(*(new int(a->getWeight()))); });
		shared_ptr<int> max_weight_value = accumulate(weight_values->begin(),
				weight_values->end(), make_shared<int>(*(new int(0))),
				[&] (shared_ptr<int> a, shared_ptr<int> b)
				{ return ((*a > *b) ? make_shared<int>(*(new int(*a))) :
						make_shared<int>(*(new int(*b)))); });
		// int next_max_weight_value = *max_weight_value;
		// return next_max_weight_value;
		return max_weight_value;
	}
}

shared_ptr<list<shared_ptr<FeedItem>>> FeedProblem::getItems() {
	return this->items;
}

int FeedProblem::_getSackCapacity() {
	return this->sack_capacity;
}

// useful for having items be ordered
// to have loss be non-decreasing from left to right
function<bool(shared_ptr<SackItem>, shared_ptr<SackItem>)>
	getNextFeedItemComp(shared_ptr<SackItem> split_sack_item) {
	// be careful about value capture
	return [&, split_sack_item] (shared_ptr<SackItem> a, shared_ptr<SackItem> b)
	{ longdouble loss_value1 = a->getLossValue(split_sack_item, true);
		longdouble loss_value2 = b->getLossValue(split_sack_item, true);
		// cout << "our split sack item for comparator: " + *(split_sack_item->toString()) << endl;
		// cout << "loss value #1: " << to_string(loss_value1) << endl;
		// cout << "loss value #2: " << to_string(loss_value2) << endl;
		return loss_value1 < loss_value2;
	};
}
shared_ptr<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>, shared_ptr<longlong>>>
	FeedProblem::solve() {
	shared_ptr<list<shared_ptr<FeedItem>>> items = this->getItems();
	// cout << "# of items in problem: " + to_string(items->size()) << endl;
	int W = this->_getSackCapacity();
	shared_ptr<longlong> R_profit = FeedProblem::_getMaxItemProfit(items);
	shared_ptr<int> R_weight = FeedProblem::_getMaxItemWeight(items);
	longlong next_R_profit = (R_profit == NULL) ? 0 : *R_profit;
	int next_R_weight = (R_weight == NULL) ? 0 : *R_weight;
	// cout << "largest profit: " + to_string(next_R_profit) << endl;
	// cout << "largest weight: " + to_string(next_R_weight) << endl;
	int n = items->size();
	shared_ptr<list<shared_ptr<SackItem>>> sack_items =
			make_shared<list<shared_ptr<SackItem>>>(*(new list<shared_ptr<SackItem>>()));
	sack_items->resize(items->size(), NULL);
	transform(items->begin(), items->end(),
			sack_items->begin(),
			[&] (shared_ptr<FeedItem> a)
			{ return make_shared<SackItem>(*(new SackItem(a->getProfit(),
					a->getWeight(), a->getIDValue()))); });
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<FeedItem>>> sack_item_to_item_dict =
			make_shared<unordered_map<shared_ptr<SackItem>,
			shared_ptr<FeedItem>>>(*(new unordered_map<shared_ptr<SackItem>, shared_ptr<FeedItem>>()));
	auto iterator1 = sack_items->begin();
	auto iterator2 = items->begin();
	while (iterator1 != sack_items->end()) {
shared_ptr<SackItem> curr_sack_item = *iterator1;
shared_ptr<FeedItem> curr_item = *iterator2;
sack_item_to_item_dict->
	insert(*(make_shared<pair<shared_ptr<SackItem>,
			shared_ptr<FeedItem>>>(*(new pair<shared_ptr<SackItem>,
					shared_ptr<FeedItem>>(curr_sack_item, curr_item)))));
		advance(iterator1, 1);
		advance(iterator2, 1);
	}
	shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>, shared_ptr<SackItem>, shared_ptr<longdouble>>> result =
			FractionalKnapsack::linearTimeFractionalSolve(sack_items, W);
	shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items;
	shared_ptr<SackItem> split_sack_item;
	shared_ptr<longdouble> split_item_fraction;
	tie(break_partial_solution_sack_items, split_sack_item, split_item_fraction) = *result;
	if (split_sack_item == NULL) {
		shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>> sack_item_list_list =
				make_shared<list<shared_ptr<list<shared_ptr<FeedItem>>>>>(*(new
						list<shared_ptr<list<shared_ptr<FeedItem>>>>()));
		shared_ptr<list<shared_ptr<SackItem>>> sack_items = break_partial_solution_sack_items;
		shared_ptr<list<shared_ptr<FeedItem>>> feed_items =
				make_shared<list<shared_ptr<FeedItem>>>(*(new list<shared_ptr<FeedItem>>()));
		feed_items->resize(sack_items->size(), NULL);
		transform(sack_items->begin(), sack_items->end(),
				feed_items->begin(),
				[&] (shared_ptr<SackItem> a)
				{ return get<1>(*(sack_item_to_item_dict->find(a))); });
		shared_ptr<list<shared_ptr<FeedItem>>> feed_item_list =
				make_shared<list<shared_ptr<FeedItem>>>(*(new list<shared_ptr<FeedItem>>()));
		for_each(feed_items->begin(), feed_items->end(),
				[&] (shared_ptr<FeedItem> a) { feed_item_list->push_back(a); });
		sack_item_list_list->push_back(feed_item_list);
		/*
		for_each(break_partial_solution_sack_items->begin(),
				break_partial_solution_sack_items->end(),
				[&] (SackItem *a) { cout << *(a->toString()) << endl; });
		*/
		shared_ptr<list<shared_ptr<longlong>>> profit_values =
				make_shared<list<shared_ptr<longlong>>>(*(new list<shared_ptr<longlong>>()));
		profit_values->resize(break_partial_solution_sack_items->size(), NULL);
		transform(break_partial_solution_sack_items->begin(),
				break_partial_solution_sack_items->end(),
				profit_values->begin(),
				[&] (shared_ptr<SackItem> a)
				{ return make_shared<longlong>(*(new longlong(a->getProfit()))); });
		/*
		for_each(profit_values->begin(), profit_values->end(),
				[&] (longlong *a) { cout << to_string(*a) << endl; });
		*/
		shared_ptr<longlong> total_profit = accumulate(profit_values->begin(),
				profit_values->end(), make_shared<longlong>(*(new longlong(0))),
				[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
				{ return make_shared<longlong>(*(new longlong(*a + *b))); });
		longlong next_total_profit = *total_profit;
		// cout << "next profit: " << next_total_profit << endl;
		shared_ptr<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>,
				shared_ptr<longlong>>> next_result =
				make_shared<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>,
				shared_ptr<longlong>>>(*(new tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>,
					shared_ptr<longlong>>(sack_item_list_list, total_profit)));
		return next_result;
	}

	// cout << "our split sack item: " + *(split_sack_item->toString()) << endl;
	shared_ptr<BreakPartialSolution> break_partial_solution =
			BreakPartialSolution::construct(break_partial_solution_sack_items,
					split_sack_item);
	/*
	list<SackItem *> *loss_ordered_sack_items =
			new list<SackItem *>(*sack_items);
	*/
	shared_ptr<vector<shared_ptr<SackItem>>> loss_ordered_sack_item_vector =
			make_shared<vector<shared_ptr<SackItem>>>(*(new vector<shared_ptr<SackItem>>()));
	for_each(sack_items->begin(), sack_items->end(),
			[&] (shared_ptr<SackItem> a) { loss_ordered_sack_item_vector->push_back(a); });
	sort(loss_ordered_sack_item_vector->begin(),
			loss_ordered_sack_item_vector->end(),
			getNextFeedItemComp(split_sack_item));
	shared_ptr<list<shared_ptr<SackItem>>> loss_ordered_sack_items =
			make_shared<list<shared_ptr<SackItem>>>(*(new list<shared_ptr<SackItem>>()));
	for_each(loss_ordered_sack_item_vector->begin(),
			loss_ordered_sack_item_vector->end(),
			[&] (shared_ptr<SackItem> a) { loss_ordered_sack_items->push_back(a); });
	shared_ptr<OriginalSackProblem> original_problem =
			make_shared<OriginalSackProblem>(*(new OriginalSackProblem(loss_ordered_sack_items,
					W, break_partial_solution)));
	original_problem->init();
	shared_ptr<list<shared_ptr<SackItem>>> solution_sack_items =
			make_shared<list<shared_ptr<SackItem>>>(*(original_problem->solve()));
	shared_ptr<list<shared_ptr<SackItem>>> sack_item_list =
			make_shared<list<shared_ptr<SackItem>>>(*(new list<shared_ptr<SackItem>>(*solution_sack_items)));
	shared_ptr<list<shared_ptr<list<shared_ptr<SackItem>>>>> sack_item_list_list =
			make_shared<list<shared_ptr<list<shared_ptr<SackItem>>>>>(*(new
					list<shared_ptr<list<shared_ptr<SackItem>>>>()));
	sack_item_list_list->push_back(sack_item_list);
	shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>> item_list_list =
			make_shared<list<shared_ptr<list<shared_ptr<FeedItem>>>>>(*(new
					list<shared_ptr<list<shared_ptr<FeedItem>>>>()));
	for (shared_ptr<list<shared_ptr<SackItem>>> sack_item_list : *sack_item_list_list) {
		shared_ptr<list<shared_ptr<FeedItem>>> item_list =
				make_shared<list<shared_ptr<FeedItem>>>(*(new list<shared_ptr<FeedItem>>()));
		for (shared_ptr<SackItem> sack_item : *sack_item_list) {
			auto iterator = sack_item_to_item_dict->find(sack_item);
			pair<shared_ptr<SackItem>, shared_ptr<FeedItem>> match = *iterator;
			shared_ptr<FeedItem> feed_item = get<1>(match);
			item_list->push_back(feed_item);
		}
		item_list_list->push_back(item_list);
	}
	shared_ptr<list<shared_ptr<longlong>>> profit_values =
			make_shared<list<shared_ptr<longlong>>>(*(new list<shared_ptr<longlong>>()));
	profit_values->resize(solution_sack_items->size(), NULL);
	transform(solution_sack_items->begin(),
			solution_sack_items->end(),
			profit_values->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return make_shared<longlong>(*(new longlong(a->getProfit()))); });
	shared_ptr<longlong> total_profit = accumulate(profit_values->begin(), profit_values->end(),
			make_shared<longlong>(*(new longlong(0))),
			[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
			{ return make_shared<longlong>(*(new longlong(*a + *b))); });
	longlong next_total_profit = *total_profit;
	// cout << "next profit: " + to_string(next_total_profit) << endl;
	shared_ptr<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>, shared_ptr<longlong>>> next_result =
			make_shared<tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>, shared_ptr<longlong>>>(*(new
					tuple<shared_ptr<list<shared_ptr<list<shared_ptr<FeedItem>>>>>,
					shared_ptr<longlong>>(item_list_list, total_profit)));
	// cout << next_total_profit << endl;
	return next_result;
}

FeedProblem::FeedProblem(shared_ptr<list<shared_ptr<FeedItem>>> feed_items, int capacity) {
	this->items = feed_items;
	this->sack_capacity = capacity;
}

FeedProblem::~FeedProblem() {
	(this->items).reset();
}

// #include "FeedOptimizer.hpp"

// #include "Solution.t.hpp"

shared_ptr<FeedProblem> FeedOptimizer::transformForMinimizingSolutionSize(shared_ptr<FeedProblem> problem) {
	// return problem;
	shared_ptr<list<shared_ptr<FeedItem>>> feed_items =
			problem->getItems();
	int capacity = problem->_getSackCapacity();
	shared_ptr<list<shared_ptr<FeedItem>>> next_items =
			make_shared<list<shared_ptr<FeedItem>>>(*(new list<shared_ptr<FeedItem>>()));
	int num_items = feed_items->size();
	for (shared_ptr<FeedItem> curr_item : *feed_items) {
		longlong curr_profit = curr_item->getProfit();
		int weight = curr_item->getWeight();
		int id_value = curr_item->getIDValue();
		longlong next_profit = curr_profit * ((longlong) num_items) - 1;
		shared_ptr<FeedItem> curr_next_item =
				make_shared<FeedItem>(*(new FeedItem(next_profit, weight, id_value)));
		next_items->push_back(curr_next_item);
	}
	shared_ptr<FeedProblem> next_problem =
			make_shared<FeedProblem>(*(new FeedProblem(next_items, capacity)));
	return next_problem;
}

shared_ptr<tuple<shared_ptr<list<shared_ptr<FeedItem>>>, shared_ptr<longlong>>>
	FeedOptimizer::untransformForMinimizingSolutionSize(shared_ptr<FeedProblem> original_problem,
		shared_ptr<FeedProblem> problem, shared_ptr<list<shared_ptr<FeedItem>>> item_collection,
		longlong total_profit) {
	/*
	tuple<list<FeedItem *> *, longlong *> *next_result =
			new tuple<list<FeedItem *> *, longlong *>(item_collection,
					new longlong(total_profit));
	// cout << "profit: " + to_string(total_profit) << endl;
	return next_result;
	*/

	shared_ptr<list<shared_ptr<FeedItem>>> feed_items = problem->getItems();
	int num_items = feed_items->size();
	shared_ptr<list<shared_ptr<FeedItem>>> next_item_collection =
			make_shared<list<shared_ptr<FeedItem>>>(*(new list<shared_ptr<FeedItem>>()));
	for (shared_ptr<FeedItem> curr_item : *item_collection) {
		longlong profit = curr_item->getProfit();
		int weight = curr_item->getWeight();
		int id_value = curr_item->getIDValue();
		longlong next_profit = (profit + (longlong) 1) / ((longlong) 1 * ((longlong) num_items));
		shared_ptr<FeedItem> next_item =
				make_shared<FeedItem>(*(new FeedItem(next_profit, weight, id_value)));
		next_item_collection->push_back(next_item);
	}
shared_ptr<list<shared_ptr<longlong>>> next_profit_values =
		make_shared<list<shared_ptr<longlong>>>(*(new list<shared_ptr<longlong>>));
next_profit_values->resize(next_item_collection->size(), NULL);
transform(next_item_collection->begin(), next_item_collection->end(),
		next_profit_values->begin(),
		[&] (shared_ptr<FeedItem> a)
		{ return make_shared<longlong>(*(new longlong(a->getProfit()))); });
shared_ptr<longlong> next_total_profit = accumulate(next_profit_values->begin(),
		next_profit_values->end(), make_shared<longlong>(*(new longlong(0))),
		[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
		{ return make_shared<longlong>(*(new longlong(*a + *b))); });
longlong result_total_profit = *next_total_profit;
// cout << to_string(result_total_profit) << endl;
shared_ptr<tuple<shared_ptr<list<shared_ptr<FeedItem>>>, shared_ptr<longlong>>> result =
		make_shared<tuple<shared_ptr<list<shared_ptr<FeedItem>>>, shared_ptr<longlong>>>(*(new
				tuple<shared_ptr<list<shared_ptr<FeedItem>>>, shared_ptr<longlong>>(next_item_collection,
				make_shared<longlong>(*(new longlong(result_total_profit))))));
return result;
	}

// #include "SackProblem.hpp"

// #include "../feed_optimizer/Solution.t.hpp"

shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> SackProblem::_getSackItemToCountDict() {
	return this->sack_item_to_count_dict;
}

shared_ptr<list<shared_ptr<SackItem>>> SackProblem::getSackItems() {
	// throw "hello";
	/*
	cout << "retrieving sack items:" << endl;
	for_each((this->loss_sorted_sack_item_list)->begin(),
			(this->loss_sorted_sack_item_list)->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << " "; });
	cout << endl;
	*/
	return this->loss_sorted_sack_item_list;
}

int SackProblem::getCapacity() {
	return this->capacity;
}

void SackProblem::setCapacity(int capacity) {
	this->capacity = capacity;
}

int SackProblem::getNumSackItems() {
	shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_item_list =
			this->loss_sorted_sack_item_list;
	int size = loss_sorted_sack_item_list->size();
	return size;
}

shared_ptr<BreakPartialSolution> SackProblem::_getBreakPartialSolution() {
	return this->break_partial_solution;
}

shared_ptr<SackItem> SackProblem::_getSplitSackItem() {
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<SackItem> split_sack_item =
			break_partial_solution->_getSplitSackItem();
	return split_sack_item;
}

shared_ptr<SackItem> SackProblem::getSackItemWithLowestLossValue() {
	shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_item_list =
			this->loss_sorted_sack_item_list;
	shared_ptr<SackItem> sack_item = loss_sorted_sack_item_list->front();
	// cout << "getting sack item with lowest loss value: " << *(sack_item->toString()) << endl;
	return sack_item;
}

void SackProblem::addSackItemWithLargeLossValue(shared_ptr<SackItem> sack_item) {
	// cout << "adding sack item with large loss value: " << *(sack_item->toString()) << endl;
	(this->loss_sorted_sack_item_list)->push_back(sack_item);
	// cout << "inserting a sack item to map" << endl;
	(this->_getSackItemToCountDict())->
			insert(*(shared_ptr<pair<shared_ptr<SackItem>, shared_ptr<int>>>(new pair<shared_ptr<SackItem>,
					shared_ptr<int>>(sack_item, shared_ptr<int>(new int(1))))));
	// cout << "next size of dictionary: " << to_string(this->_getSackItemToCountDict()->size()) << endl;
}

void SackProblem::removeSackItemWithLowestLossValue() {
	shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_item_list =
			this->loss_sorted_sack_item_list;
	shared_ptr<SackItem> removed_sack_item = loss_sorted_sack_item_list->front();
	loss_sorted_sack_item_list->pop_front();
	(this->_getSackItemToCountDict())->erase(removed_sack_item);
	// cout << "removing sack item with low loss value: " << *(removed_sack_item->toString()) << endl;
}

bool SackProblem::hasSackItem(shared_ptr<S> sack_item) {
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			this->_getSackItemToCountDict();
	bool has_sack_item = sack_item_to_count_dict->count(sack_item) != 0;
	/*
	cout << "ran init. flag value: " + to_string(this->ran_init) << endl;
	cout << "dictionary size: " + to_string(sack_item_to_count_dict->size()) << endl;
	cout << "looking for sack item: " + *(sack_item->toString()) << endl;
	*/
	/*
	for_each(sack_item_to_count_dict->begin(), sack_item_to_count_dict->end(),
			[&] (tuple<SackItem *, int *> a)
			{ cout << "existing item: " + *(get<0>(a)->toString()) << endl; });
	*/
	// cout << "have sack item: " + to_string(has_sack_item) << endl;

	/*
	bool has_sack_item = (sack_item_to_count_dict->find(sack_item)
			== sack_item_to_count_dict->end()) == false;
	*/

	/*
	if (sack_item_to_count_dict->find(sack_item) != sack_item_to_count_dict->end()) {
		throw "found a match";
	}
	*/
	return has_sack_item;
}

shared_ptr<list<shared_ptr<SackItem>>> SackProblem::_getItemsSortedByLossValue() {
	shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_item_list =
			this->loss_sorted_sack_item_list;
	return loss_sorted_sack_item_list;
}

SackProblem::SackProblem(shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_items,
		int capacity, shared_ptr<BreakPartialSolution> break_partial_solution) {
	this->loss_sorted_sack_item_list =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*loss_sorted_sack_items));
	// cout << "# of loss-sorted sack items: " + to_string(this->loss_sorted_sack_item_list->size()) << endl;
	// cout << "next # of loss-sorted sack items: " + to_string(loss_sorted_sack_items->size()) << endl;
	this->capacity = capacity;
	this->break_partial_solution = break_partial_solution;
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>>(new
					unordered_map<shared_ptr<SackItem>, shared_ptr<int>>());
	this->sack_item_to_count_dict = sack_item_to_count_dict;
	this->ran_init = false;
}

void SackProblem::init() {
	shared_ptr<unordered_map<shared_ptr<SackItem>, shared_ptr<int>>> sack_item_to_count_dict =
			this->sack_item_to_count_dict;
	shared_ptr<list<shared_ptr<SackItem>>> loss_sorted_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*(this->loss_sorted_sack_item_list)));
	// less than desirable work-around so we don't
	// doubly include particular sack items
	this->loss_sorted_sack_item_list = shared_ptr<list<shared_ptr<SackItem>>>(new
			list<shared_ptr<SackItem>>());
	// cout << to_string(loss_sorted_sack_items->size()) << endl;
	auto iterator = loss_sorted_sack_items->begin();
	// for (SackItem *sack_item : *loss_sorted_sack_items) {
	for(int i = 0; i < (int) loss_sorted_sack_items->size(); i++) {
		shared_ptr<SackItem> sack_item = *iterator;
		// be careful not to add while we consume
		this->addSackItemWithLargeLossValue(sack_item);
		/*
		cout << "added a sack item to a sack problem" << endl;
		cout << *(sack_item->toString()) << endl;
		*/
		advance(iterator, 1);
	}
	this->ran_init = true;
}

SackProblem::~SackProblem() {
	(this->break_partial_solution).reset();
	(this->loss_sorted_sack_item_list).reset();
	(this->sack_item_to_count_dict).reset();
}

/*
using S = SackItem;
using N = DoublyLinkedListNode<S>;
using L = DoublyLinkedList<S>;
unordered_map<S *, int *> *_getSackItemToCountDict();
list<S *> *getSackItems();
list<S *> *getSackItemsOrderedByLossValue();
int getCapacity();
void setCapacity(int capacity);
int getNumSackItems();
BreakPartialSolution *_getBreakPartialSolution();
S *_getSplitSackItem();
S *getSackItemWithLowestLossValue();
void addSackItemWithLargeLossValue(S *sack_item);
void removeSackItemWithLowestLossValue();
list<S *> *_getItemsSortedByLossValue();

*/

// #include "SackSubproblem.hpp"

class SackProblem;

shared_ptr<SackProblem> SackSubproblem::getSourceProblem() {
	return (this->source_problem).lock();
}

SackSubproblem::SackSubproblem(shared_ptr<SackProblem> source_problem,
		shared_ptr<list<shared_ptr<SackItem>>> sack_items,
		int capacity, shared_ptr<BreakPartialSolution> break_partial_solution)
	: SackProblem(sack_items, capacity, break_partial_solution) {
	this->source_problem = weak_ptr<SackProblem>(source_problem);
}

SackSubproblem::~SackSubproblem() {
	(this->source_problem).reset();
}

/*

#include "NonCoreSackSubproblem.hpp"

#include "CoreSackSubproblem.hpp"

#include "OriginalSackProblem.hpp"

*/

shared_ptr<SackItem> NonCoreSackSubproblem::getItemWithLowestLossValue() {
	shared_ptr<list<shared_ptr<SackItem>>> sack_item_list = this->_getItemsSortedByLossValue();
	shared_ptr<SackItem> chosen_sack_item = sack_item_list->front();
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	longdouble loss_value = chosen_sack_item->getLossValue(split_sack_item, true);
	return chosen_sack_item;
}

shared_ptr<PartialSolution> NonCoreSackSubproblem::solve() {
shared_ptr<BreakPartialSolution> break_partial_solution = this->_getBreakPartialSolution();
shared_ptr<list<shared_ptr<SackItem>>> sack_items = this->getSackItems();
shared_ptr<OriginalSackProblem> original_problem =
		static_pointer_cast<OriginalSackProblem>(this->getSourceProblem());
shared_ptr<CoreSackSubproblem> core_subproblem = original_problem->getCoreSubproblem();
shared_ptr<list<shared_ptr<SackItem>>> core_sack_items = core_subproblem->getSackItems();
shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
shared_ptr<list<shared_ptr<SackItem>>> chosen_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items));
chosen_items->erase(remove_if(chosen_items->begin(), chosen_items->end(),
		[&] (shared_ptr<SackItem> a) { return break_partial_solution->hasSackItem(a) == false; }),
		chosen_items->end());
shared_ptr<list<shared_ptr<SackItem>>> core_break_solution_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*core_sack_items));
core_break_solution_items->erase(remove_if(core_break_solution_items->begin(),
		core_break_solution_items->end(),
		[&] (shared_ptr<SackItem> a) { return break_partial_solution->hasSackItem(a) == false; }),
		core_break_solution_items->end());
shared_ptr<list<shared_ptr<longdouble>>> loss_values =
		shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
loss_values->resize(core_break_solution_items->size(), NULL);
transform(core_break_solution_items->begin(), core_break_solution_items->end(),
		loss_values->begin(), [&] (shared_ptr<SackItem> a)
		{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
shared_ptr<longdouble> base_loss_value = accumulate(loss_values->begin(), loss_values->end(),
		shared_ptr<longdouble>(new longdouble(0)), [&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
		{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
longdouble next_base_loss_value = *base_loss_value;
shared_ptr<P> partial_solution =
		PartialSolution::construct(chosen_items,
				split_sack_item, break_partial_solution,
				next_base_loss_value, shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>()));
return partial_solution;

}

shared_ptr<string> NonCoreSackSubproblem::toString() {
	shared_ptr<string> result_str = shared_ptr<string>(new string(""));
	shared_ptr<list<shared_ptr<SackItem>>> sack_items = this->getSackItems();
	for_each(sack_items->begin(), sack_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ result_str = shared_ptr<string>(new string(*result_str + *(a->toString()) + " ")); });
	return result_str;
}

NonCoreSackSubproblem::NonCoreSackSubproblem(shared_ptr<SackProblem> source_problem,
		shared_ptr<list<shared_ptr<SackItem>>> sack_items, int capacity,
		shared_ptr<BreakPartialSolution> break_partial_solution)
	: SackSubproblem(source_problem, sack_items, capacity, break_partial_solution) {
	/*
	cout << "created a non-core sack problem with following items:" << endl;
	for_each(sack_items->begin(), sack_items->end(),
			[&] (SackItem *a) { cout << "non-core item: " << *(a->toString()) << endl; });
	*/
}

NonCoreSackSubproblem::~NonCoreSackSubproblem() {
	// cout << "destructing a non-core sack sub-problem" << endl;
}

/*

#include "NonCoreSackSubproblem.hpp"

#include "CoreSackSubproblem.hpp"

#include "OriginalSackProblem.hpp"

*/

// #include "CoreSackSubproblem.hpp"

// #include "../knapsack/ListDecomposition.hpp"

using P_p = PostListDecomposeSubproblem;

using P = PartialSolution;

using A = PartialSolutionPathLabel;

shared_ptr<P_p> CoreSackSubproblem::getLeftPostListDecomposeSubproblem() {
	return this->left_post_list_decompose_subproblem;
}

shared_ptr<P_p> CoreSackSubproblem::getRightPostListDecomposeSubproblem() {
	return this->right_post_list_decompose_subproblem;
}

void CoreSackSubproblem::setLeftPostListDecomposeSubproblem(shared_ptr<P_p> problem) {
	this->left_post_list_decompose_subproblem = problem;
}

void CoreSackSubproblem::setRightPostListDecomposeSubproblem(shared_ptr<P_p> problem) {
	this->right_post_list_decompose_subproblem = problem;
}

shared_ptr<list<shared_ptr<SackItem>>> CoreSackSubproblem::
	getAssumeIncludedBreakPartialSolutionSackItems(shared_ptr<P_p> problem) {
	shared_ptr<OriginalSackProblem> source_problem =
			static_pointer_cast<OriginalSackProblem>(this->getSourceProblem());
	shared_ptr<NonCoreSackSubproblem> non_core_subproblem =
			source_problem->getNonCoreSubproblem();
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items =
			break_partial_solution->getSackItems();
	/*
	 cout << string("number of break partial solution sack items: ") +
		to_string(break_partial_solution_sack_items->size()) << endl;
	*/
	/*
	for_each(break_partial_solution_sack_items->begin(),
			break_partial_solution_sack_items->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << endl; });
	*/
	shared_ptr<list<shared_ptr<SackItem>>> problem_sack_items = problem->getSackItems();
	// cout << "post-list-decompose subproblem sack items: " << endl;
	/*
	for_each(problem_sack_items->begin(), problem_sack_items->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << endl; });
	*/
	shared_ptr<list<shared_ptr<SackItem>>> assume_included_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*break_partial_solution_sack_items));
	assume_included_sack_items->erase(remove_if(assume_included_sack_items->begin(),
			assume_included_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return (problem->hasSackItem(a)) == false; }),
				assume_included_sack_items->end());
	// cout << to_string(problem->hasSackItem(a)) << endl;
	// cout << "# of assume included sack items: " + to_string(assume_included_sack_items->size()) << endl;
	return assume_included_sack_items;
}

shared_ptr<list<shared_ptr<SackItem>>> CoreSackSubproblem::
	getAssumeNotIncludedBreakPartialSolutionSackItems(shared_ptr<P_p> problem) {
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items =
			break_partial_solution->getSackItems();
	shared_ptr<list<shared_ptr<SackItem>>> assume_not_included_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*break_partial_solution_sack_items));
	assume_not_included_sack_items->erase(remove_if(assume_not_included_sack_items->begin(),
			assume_not_included_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return (problem->hasSackItem(a) == false) == false; }),
				assume_not_included_sack_items->end());
	return assume_not_included_sack_items;
}

shared_ptr<P_p> CoreSackSubproblem::_getLeftPostListDecomposeSubproblem() {
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*(this->_getItemsSortedByLossValue())));
	int num_sack_items = this->getNumSackItems();
	int num_left_sack_items = (int) floor(num_sack_items / 2.0);
	// num_left_sack_items = num_sack_items;
	shared_ptr<list<shared_ptr<SackItem>>> left_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	auto start_it = sorted_sack_items->begin();
	auto finish_it = sorted_sack_items->begin();
	advance(finish_it, num_left_sack_items);
	left_sack_items->splice(left_sack_items->end(), *sorted_sack_items,
			start_it, finish_it);
	/*
	cout << "left post-list-decompose subproblem sack items:" << endl;
	for_each(left_sack_items->begin(), left_sack_items->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << endl; });
	*/
	shared_ptr<CoreSackSubproblem> source_problem =
			static_pointer_cast<CoreSackSubproblem>(shared_from_this());
	int capacity = this->getCapacity();
	shared_ptr<BreakPartialSolution> break_partial_solution = this->_getBreakPartialSolution();
	/*
	shared_ptr<P_p> left_subproblem =
			make_shared<P_p>(*(new PostListDecomposeSubproblem(source_problem,
				left_sack_items, capacity, break_partial_solution, true)));
	*/
	shared_ptr<P_p> left_subproblem =
			shared_ptr<P_p>(new PostListDecomposeSubproblem(source_problem,
				left_sack_items, capacity, break_partial_solution, true));
	left_subproblem->init();
	return left_subproblem;
}

shared_ptr<P_p> CoreSackSubproblem::_getRightPostListDecomposeSubproblem() {
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>((*this->_getItemsSortedByLossValue())));
	int num_sack_items = this->getNumSackItems();
	int num_left_sack_items = (int) floor(num_sack_items / 2.0);
	// num_left_sack_items = num_sack_items;
	int num_right_sack_items = num_sack_items - num_left_sack_items;
	shared_ptr<list<shared_ptr<SackItem>>> next_sorted_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*sorted_sack_items));
	next_sorted_sack_items->reverse();
	auto start_it = next_sorted_sack_items->begin();
	auto finish_it = next_sorted_sack_items->begin();
	advance(finish_it, num_right_sack_items);
	shared_ptr<list<shared_ptr<SackItem>>> reversed_right_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
	reversed_right_sack_items->splice(reversed_right_sack_items->end(),
			*next_sorted_sack_items,
			start_it, finish_it);
	shared_ptr<list<shared_ptr<SackItem>>> right_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>(*reversed_right_sack_items));
	right_sack_items->reverse();
	/*
	cout << "right post-list-decompose subproblem sack items:" << endl;
	for_each(right_sack_items->begin(), right_sack_items->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << endl; });
	*/
	shared_ptr<CoreSackSubproblem> source_problem =
			static_pointer_cast<CoreSackSubproblem>(shared_from_this());
	int capacity = this->getCapacity();
	shared_ptr<BreakPartialSolution> break_partial_solution = this->_getBreakPartialSolution();
	/*
	shared_ptr<P_p> right_subproblem =
			make_shared<P_p>(*(new PostListDecomposeSubproblem(source_problem,
					right_sack_items, capacity, break_partial_solution, false)));
	*/
	shared_ptr<P_p> right_subproblem =
			shared_ptr<P_p>(new PostListDecomposeSubproblem(source_problem,
					right_sack_items, capacity, break_partial_solution, false));
	right_subproblem->init();
	// cout << "post-list-decompose sub-problem use count: " << right_subproblem.use_count() << endl;
	return right_subproblem;
}

shared_ptr<tuple<shared_ptr<P_p>, shared_ptr<P_p>>> CoreSackSubproblem::divideIntoLeftAndRight() {
	// cout << "pre-divide core sack items: " + *(this->toString()) << endl;
	shared_ptr<P_p> left_subproblem = this->_getLeftPostListDecomposeSubproblem();
	shared_ptr<P_p> right_subproblem = this->_getRightPostListDecomposeSubproblem();
	// cout << "post-divide core sack items: " + *(this->toString()) << endl;
	this->setLeftPostListDecomposeSubproblem(left_subproblem);
	this->setRightPostListDecomposeSubproblem(right_subproblem);
	/*
	shared_ptr<tuple<shared_ptr<P_p>, shared_ptr<P_p>>> result =
			make_shared<tuple<shared_ptr<P_p>, shared_ptr<P_p>>>(*(new
					tuple<shared_ptr<P_p>, shared_ptr<P_p>>(left_subproblem, right_subproblem)));
	*/
	shared_ptr<tuple<shared_ptr<P_p>, shared_ptr<P_p>>> result =
			shared_ptr<tuple<shared_ptr<P_p>, shared_ptr<P_p>>>(new
					tuple<shared_ptr<P_p>, shared_ptr<P_p>>(left_subproblem, right_subproblem));
	return result;
}

shared_ptr<P> CoreSackSubproblem::
	getPostListDecomposeSubproblemStarterPartialSolution(shared_ptr<P_p> problem,
		bool is_left_portion) {
	shared_ptr<list<shared_ptr<SackItem>>> include_sack_items =
			this->getAssumeIncludedBreakPartialSolutionSackItems(problem);
	// cout << "included sack items: " << endl;
	/*
	for_each(include_sack_items->begin(), include_sack_items->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << endl; });
	*/
	shared_ptr<list<shared_ptr<SackItem>>> not_include_sack_items =
			this->getAssumeNotIncludedBreakPartialSolutionSackItems(problem);
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	shared_ptr<list<shared_ptr<longdouble>>> loss_values =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	loss_values->resize(not_include_sack_items->size(), NULL);
	transform(not_include_sack_items->begin(), not_include_sack_items->end(),
			loss_values->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
	shared_ptr<longdouble> total_loss_value = accumulate(loss_values->begin(),
			loss_values->end(), shared_ptr<longdouble>(new longdouble(0)),
			[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
			{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	longdouble next_total_loss_value = *total_loss_value;
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	longdouble base_loss_value = next_total_loss_value;
	shared_ptr<P> partial_solution =
			PartialSolution::
			construct(include_sack_items, split_sack_item,
					break_partial_solution, base_loss_value,
					shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>()));
	/*
	cout << string("retrieving a starter partial solution ")
			+ string("and specifying that it has # of included sack items: ")
			+ to_string(include_sack_items->size()) << endl;
	*/
	return partial_solution;
}

shared_ptr<P> CoreSackSubproblem::combineSolutionsForLeftAndRight(shared_ptr<list<shared_ptr<P>>> left_partial_solutions,
		shared_ptr<list<shared_ptr<P>>> right_partial_solutions) {
	shared_ptr<OriginalSackProblem> original_problem =
			static_pointer_cast<OriginalSackProblem>(this->getSourceProblem());
	shared_ptr<NonCoreSackSubproblem> non_core_subproblem =
			original_problem->getNonCoreSubproblem();
	shared_ptr<P_p> left_subproblem = this->getLeftPostListDecomposeSubproblem();
	shared_ptr<P_p> right_subproblem = this->getRightPostListDecomposeSubproblem();
	int capacity = this->getCapacity();
	shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>> best_partial_solution_pair =
			ListDecomposition::getABestPair(left_partial_solutions,
				right_partial_solutions, capacity,
				non_core_subproblem, left_subproblem,
				right_subproblem);
	shared_ptr<P> left_partial_solution;
	shared_ptr<P> right_partial_solution;
	tie(left_partial_solution, right_partial_solution) =
			*best_partial_solution_pair;

	/*

	cout << "pair left partial solution:" << endl;
	cout << *(left_partial_solution->toString()) << endl;
	cout << "pair right partial solution:" << endl;
	cout << *(right_partial_solution->toString()) << endl;

	*/

	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();

	/*

	cout << "pair left partial solution sack items:" << endl;
	cout << to_string(left_partial_solution->getSackItems()->size()) << endl;
	cout << "pair right partial solution sack items:" << endl;
	cout << to_string(right_partial_solution->getSackItems()->size()) << endl;
	cout << "pair left partial solution item count:" << endl;
	cout << to_string(left_partial_solution->sack_item_count) << endl;
	cout << "pair right partial solution item count:" << endl;
	cout << to_string(right_partial_solution->sack_item_count) << endl;
	cout << "pair left partial solution contained items:" << endl;
	cout << *(left_partial_solution->toExtendedString()) << endl;
	cout << "pair right partial solution contained items:" << endl;
	cout << *(right_partial_solution->toExtendedString()) << endl;

	*/

	shared_ptr<P> partial_solution =
			PartialSolution::
			_combinePartialSolutions(left_partial_solution,
					right_partial_solution, split_sack_item,
					this->_getBreakPartialSolution(), left_subproblem,
					right_subproblem);
	// cout << "combined partial solution:" << endl;
	// cout << *(partial_solution->toExtendedString()) << endl;
	return partial_solution;

}



shared_ptr<P> CoreSackSubproblem::combineSolutionsForLeftAndRightBruteForce(shared_ptr<list<shared_ptr<P>>> left_partial_solutions,
		shared_ptr<list<shared_ptr<P>>> right_partial_solutions) {
	shared_ptr<P_p> left_subproblem = this->getLeftPostListDecomposeSubproblem();
	shared_ptr<P_p> right_subproblem = this->getRightPostListDecomposeSubproblem();
	int capacity = this->getCapacity();
	longdouble best_profit = 0;
	shared_ptr<list<shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>>>> best_partial_solution_pairs =
			shared_ptr<list<shared_ptr<tuple<shared_ptr<P>,
			shared_ptr<P>>>>>(new list<shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>>>());
	for (shared_ptr<P> left_partial_solution : *left_partial_solutions) {
		for (shared_ptr<P> right_partial_solution : *right_partial_solutions) {
longlong left_profit = left_partial_solution->getTotalProfit();
int left_weight = left_partial_solution->getTotalWeight();
longlong right_profit = right_partial_solution->getTotalProfit();
int right_weight = right_partial_solution->getTotalWeight();
shared_ptr<list<shared_ptr<SackItem>>> left_partial_solution_sack_items =
		left_partial_solution->getSackItems();
shared_ptr<list<shared_ptr<SackItem>>> right_partial_solution_sack_items =
		right_partial_solution->getSackItems();
auto left_start_it = left_partial_solution_sack_items->begin();
auto left_finish_it = left_partial_solution_sack_items->end();
auto right_start_it = right_partial_solution_sack_items->begin();
auto right_finish_it = right_partial_solution_sack_items->end();
shared_ptr<set<shared_ptr<SackItem>>> left_item_set =
		shared_ptr<set<shared_ptr<SackItem>>>(new set<shared_ptr<SackItem>>());
shared_ptr<set<shared_ptr<SackItem>>> right_item_set =
		shared_ptr<set<shared_ptr<SackItem>>>(new set<shared_ptr<SackItem>>());
left_item_set->insert(left_start_it, left_finish_it);
right_item_set->insert(right_start_it, right_finish_it);
// find an intersection
shared_ptr<list<shared_ptr<SackItem>>> shared_item_list =
		shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>());
// make space for intersection
shared_item_list->resize(left_item_set->size() + right_item_set->size(), NULL);
set_union(left_item_set->begin(), left_item_set->end(),
		right_item_set->begin(), right_item_set->end(),
		shared_item_list->end());
shared_item_list->erase(remove_if(shared_item_list->begin(),
		shared_item_list->end(),
		[&] (shared_ptr<SackItem> a) { return a == NULL; }),
		shared_item_list->end());
shared_ptr<list<shared_ptr<int>>> shared_weight_values =
		shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
shared_ptr<list<shared_ptr<longlong>>> shared_profit_values =
		shared_ptr<list<shared_ptr<longlong>>>(new list<shared_ptr<longlong>>());
shared_ptr<int> shared_weight = accumulate(shared_weight_values->begin(),
		shared_weight_values->end(), shared_ptr<int>(new int(0)),
		[&] (shared_ptr<int> a, shared_ptr<int> b)
		{ return shared_ptr<int>(new int(*a + *b)); });
shared_ptr<longlong> shared_profit = accumulate(shared_profit_values->begin(),
		shared_profit_values->end(), shared_ptr<longlong>(new longlong(0)),
		[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
		{ return shared_ptr<longlong>(new longlong(*a + *b)); });
int next_shared_weight = *shared_weight;
longlong next_shared_profit = *shared_profit;
int combined_weight = left_weight + right_weight - next_shared_weight;
longlong combined_profit = left_profit + right_profit - next_shared_profit;
shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>> curr_partial_solution_pair =
		shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>>(new tuple<shared_ptr<P>,
				shared_ptr<P>>(left_partial_solution, right_partial_solution));
if (combined_weight <= capacity) {
	if (combined_profit > best_profit) {
		best_partial_solution_pairs =
				shared_ptr<list<shared_ptr<tuple<shared_ptr<P>,
				shared_ptr<P>>>>>(new list<shared_ptr<tuple<shared_ptr<P>,
						shared_ptr<P>>>>());
		best_partial_solution_pairs->push_back(curr_partial_solution_pair);
		best_profit = combined_profit;
	} else if (combined_profit == best_profit) {
		best_partial_solution_pairs->push_back(curr_partial_solution_pair);
	}
}
		}
	}

shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
shared_ptr<list<shared_ptr<P>>> partial_solutions =
		shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
partial_solutions->resize(best_partial_solution_pairs->size(), NULL);
transform(best_partial_solution_pairs->begin(),
		best_partial_solution_pairs->end(),
		partial_solutions->begin(),
		[&] (shared_ptr<tuple<shared_ptr<P>, shared_ptr<P>>> a)
		{ shared_ptr<P> b; shared_ptr<P> c; tie(b, c) = *a;
		return PartialSolution::_combinePartialSolutions(b,
				c, split_sack_item, this->_getBreakPartialSolution(),
				left_subproblem, right_subproblem); });
shared_ptr<list<shared_ptr<P>>> candidate_partial_solutions = partial_solutions;
shared_ptr<list<shared_ptr<A>>> path_label_list =
		shared_ptr<list<shared_ptr<A>>>(new list<shared_ptr<A>>());
path_label_list->resize(candidate_partial_solutions->size(), NULL);
transform(candidate_partial_solutions->begin(),
		candidate_partial_solutions->end(),
		path_label_list->begin(),
		[&] (shared_ptr<P> a) { return a->toPartialSolutionPathLabel(); } );
shared_ptr<A> best_path_label = PartialSolutionPathLabel::getMin(path_label_list);
shared_ptr<list<shared_ptr<P>>> next_candidate_partial_solutions =
		shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*candidate_partial_solutions));
next_candidate_partial_solutions->
erase(remove_if(next_candidate_partial_solutions->begin(),
		next_candidate_partial_solutions->end(),
		[&] (shared_ptr<P> a) { return (a->toPartialSolutionPathLabel()->
				isEqualTo(best_path_label)) == false; }),
		next_candidate_partial_solutions->end());
shared_ptr<P> chosen_partial_solution = next_candidate_partial_solutions->front();
shared_ptr<P> partial_solution = chosen_partial_solution;
return partial_solution;

}

shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> CoreSackSubproblem::
	iterateSolve(shared_ptr<IntegralityGapEstimate> integrality_gap_estimate,
		longlong non_core_subproblem_partial_solution_profit,
		int work_done_by_right, shared_ptr<NonCoreSackSubproblem> non_core_subproblem) {
	shared_ptr<P_p> left_subproblem = this->getLeftPostListDecomposeSubproblem();
	shared_ptr<P_p> right_subproblem = this->getRightPostListDecomposeSubproblem();
	shared_ptr<SackItem> split_sack_item =
			this->_getSplitSackItem();
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items =
		break_partial_solution->getSackItems();
shared_ptr<list<shared_ptr<SackItem>>> left_subproblem_break_solution_sack_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new
				list<shared_ptr<SackItem>>(*break_partial_solution_sack_items));
left_subproblem_break_solution_sack_items->
	erase(remove_if(left_subproblem_break_solution_sack_items->begin(),
		left_subproblem_break_solution_sack_items->end(),
		[&] (shared_ptr<SackItem> a) { return (left_subproblem->hasSackItem(a)) == false; }),
		left_subproblem_break_solution_sack_items->end());
shared_ptr<list<shared_ptr<SackItem>>> right_subproblem_break_solution_sack_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new
				list<shared_ptr<SackItem>>(*break_partial_solution_sack_items));
right_subproblem_break_solution_sack_items->
	erase(remove_if(right_subproblem_break_solution_sack_items->begin(),
			right_subproblem_break_solution_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return (right_subproblem->hasSackItem(a)) == false; }),
					right_subproblem_break_solution_sack_items->end());
if (left_subproblem->isFinished() == false) {
	shared_ptr<SackItem> next_left_sack_item =
			left_subproblem->getNextRemainingItemBasedOnIsStarterItemAndLossValue();
	left_subproblem->removeNextRemainingItemBasedOnIsStarterItemAndLossValue();
	left_subproblem->iterateSolve(next_left_sack_item,
			integrality_gap_estimate, non_core_subproblem);
}
shared_ptr<list<shared_ptr<P>>> left_L_curr = left_subproblem->_getCurrentWinnowedParetoPoints();
shared_ptr<list<shared_ptr<longdouble>>> left_starter_solution_loss_values =
		shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
left_starter_solution_loss_values->resize(left_subproblem_break_solution_sack_items->size(), NULL);
transform(left_subproblem_break_solution_sack_items->begin(),
		left_subproblem_break_solution_sack_items->end(),
		left_starter_solution_loss_values->begin(),
		[&] (shared_ptr<SackItem> a)
		{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
shared_ptr<list<shared_ptr<P>>> right_L_curr = right_subproblem->_getCurrentWinnowedParetoPoints();
shared_ptr<list<shared_ptr<longdouble>>> right_starter_solution_loss_values =
		shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
right_starter_solution_loss_values->resize(right_subproblem_break_solution_sack_items->size(), NULL);
transform(right_subproblem_break_solution_sack_items->begin(),
		right_subproblem_break_solution_sack_items->end(),
		right_starter_solution_loss_values->begin(),
		[&] (shared_ptr<SackItem> a)
		{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
	shared_ptr<longdouble> left_starter_solution_base_loss_value =
			accumulate(left_starter_solution_loss_values->begin(),
					left_starter_solution_loss_values->end(),
					shared_ptr<longdouble>(new longdouble(0)),
					[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
					{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	shared_ptr<longdouble> right_starter_solution_base_loss_value =
			accumulate(right_starter_solution_loss_values->begin(),
					right_starter_solution_loss_values->end(),
					shared_ptr<longdouble>(new longdouble(0)),
					[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
					{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	longdouble next_left_starter_solution_base_loss_value =
			*left_starter_solution_base_loss_value;
	shared_ptr<P> left_added_partial_solution =
			PartialSolution::construct(shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>()),
					split_sack_item, break_partial_solution,
					next_left_starter_solution_base_loss_value,
					shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>()));
	longdouble next_right_starter_solution_base_loss_value =
			*right_starter_solution_base_loss_value;
	shared_ptr<P> right_added_partial_solution =
			PartialSolution::construct(shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>()),
					split_sack_item, break_partial_solution,
					next_right_starter_solution_base_loss_value,
					shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>()));
	if (left_subproblem->isFinished() == true && right_subproblem->isFinished() == false) {
		shared_ptr<SackItem> next_right_sack_item =
				right_subproblem->getNextRemainingItemBasedOnIsStarterItemAndLossValue();
		right_subproblem->removeNextRemainingItemBasedOnIsStarterItemAndLossValue();
		right_subproblem->iterateSolve(next_right_sack_item,
				integrality_gap_estimate, non_core_subproblem);
	}
	shared_ptr<list<shared_ptr<P>>> next_left_L_curr =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*left_L_curr));
	next_left_L_curr->push_front(left_added_partial_solution);
	shared_ptr<list<shared_ptr<P>>> next_right_L_curr =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*right_L_curr));
	next_right_L_curr->push_front(right_added_partial_solution);
	int next_work_done_by_right = work_done_by_right + right_L_curr->size();
	shared_ptr<int> next_work_done_by_right_shared_ptr =
			shared_ptr<int>(new int(next_work_done_by_right));
	if (next_work_done_by_right >= left_L_curr->size()) {
		next_work_done_by_right = next_work_done_by_right - left_L_curr->size();
		shared_ptr<P> partial_solution =
				this->combineSolutionsForLeftAndRight(next_left_L_curr,
						next_right_L_curr);
		longlong curr_max_core_profit = partial_solution->getTotalProfit();
		longlong curr_overall_profit =
				curr_max_core_profit + non_core_subproblem_partial_solution_profit;
		integrality_gap_estimate->updateBestIntegerSolutionProfit(curr_overall_profit);
		shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> result =
				shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>(new
						tuple<shared_ptr<P>, shared_ptr<int>>(partial_solution,
								next_work_done_by_right_shared_ptr));
		return result;
	} else {
		shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> result =
				shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>>(new
						tuple<shared_ptr<P>, shared_ptr<int>>(NULL,
								next_work_done_by_right_shared_ptr));
		return result;
	}
}

shared_ptr<P> CoreSackSubproblem::
	solve(shared_ptr<IntegralityGapEstimate> integrality_gap_estimate,
		longlong non_core_subproblem_partial_solution_profit) {
	shared_ptr<OriginalSackProblem> original_problem =
			static_pointer_cast<OriginalSackProblem>(this->getSourceProblem());
	shared_ptr<NonCoreSackSubproblem> non_core_subproblem =
			original_problem->getNonCoreSubproblem();
	// cout << "pre-attempt-solve core sack items: " + *(this->toString()) << endl;
	shared_ptr<P_p> left_subproblem;
	shared_ptr<P_p> right_subproblem;
	tie(left_subproblem, right_subproblem) = *(this->divideIntoLeftAndRight());
	shared_ptr<P> curr_partial_solution = NULL;
	int curr_work_done_by_right = 0;
while ((left_subproblem->isFinished() == false)
		|| (right_subproblem->isFinished() == false)) {
	// cout << "pre-iterate-solve core sack items: " + *(this->toString()) << endl;
shared_ptr<tuple<shared_ptr<P>, shared_ptr<int>>> result =
		this->iterateSolve(integrality_gap_estimate,
				non_core_subproblem_partial_solution_profit,
				curr_work_done_by_right, non_core_subproblem);
	shared_ptr<P> partial_solution;
	shared_ptr<int> work_done_by_right_shared_ptr;
	int work_done_by_right;
tie(partial_solution, work_done_by_right_shared_ptr) = *result;
work_done_by_right = *work_done_by_right_shared_ptr;
curr_work_done_by_right = work_done_by_right;

}

// do nothing with partial solution
shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
shared_ptr<BreakPartialSolution> break_partial_solution =
		this->_getBreakPartialSolution();
shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items =
		break_partial_solution->getSackItems();

shared_ptr<list<shared_ptr<SackItem>>> left_subproblem_break_solution_sack_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new
				list<shared_ptr<SackItem>>(*break_partial_solution_sack_items));
left_subproblem_break_solution_sack_items->
	erase(remove_if(left_subproblem_break_solution_sack_items->begin(),
			left_subproblem_break_solution_sack_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ return (left_subproblem->hasSackItem(a))
					== false; }),
					left_subproblem_break_solution_sack_items->end());

shared_ptr<list<shared_ptr<SackItem>>> right_subproblem_break_solution_sack_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new
				list<shared_ptr<SackItem>>(*break_partial_solution_sack_items));
right_subproblem_break_solution_sack_items->
	erase(remove_if(right_subproblem_break_solution_sack_items->begin(),
			right_subproblem_break_solution_sack_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ return (right_subproblem->hasSackItem(a))
					== false; }),
					right_subproblem_break_solution_sack_items->end());

	shared_ptr<list<shared_ptr<P>>> left_winnowed_partial_solutions =
			left_subproblem->_getCurrentWinnowedParetoPoints();
	shared_ptr<list<shared_ptr<longdouble>>> right_loss_values =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	right_loss_values->resize(right_subproblem_break_solution_sack_items->size(), NULL);
	transform(right_subproblem_break_solution_sack_items->begin(),
			right_subproblem_break_solution_sack_items->end(),
			right_loss_values->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return shared_ptr<longdouble>(new longdouble (a->getLossValue(split_sack_item, true))); });
	shared_ptr<longdouble> left_base_loss_value =
			accumulate(right_loss_values->begin(),
					right_loss_values->end(), shared_ptr<longdouble>(new longdouble(0)),
					[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
					{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	longdouble next_left_base_loss_value = *left_base_loss_value;

	shared_ptr<P> added_left_partial_solution =
			PartialSolution::construct(shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>()),
					split_sack_item, break_partial_solution,
					next_left_base_loss_value, shared_ptr<list<shared_ptr<P>>>(new
							list<shared_ptr<P>>()));

	shared_ptr<list<shared_ptr<P>>> next_left_winnowed_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new
					list<shared_ptr<P>>(*left_winnowed_partial_solutions));
	next_left_winnowed_partial_solutions->push_front(added_left_partial_solution);

	shared_ptr<list<shared_ptr<P>>> right_winnowed_partial_solutions =
			right_subproblem->_getCurrentWinnowedParetoPoints();
	shared_ptr<list<shared_ptr<longdouble>>> left_loss_values =
			shared_ptr<list<shared_ptr<longdouble>>>(new list<shared_ptr<longdouble>>());
	left_loss_values->resize(left_subproblem_break_solution_sack_items->size(), NULL);
	transform(left_subproblem_break_solution_sack_items->begin(),
			left_subproblem_break_solution_sack_items->end(),
			left_loss_values->begin(),
			[&] (shared_ptr<SackItem> a)
			{ return shared_ptr<longdouble>(new longdouble(a->getLossValue(split_sack_item, true))); });
	shared_ptr<longdouble> right_base_loss_value =
			accumulate(left_loss_values->begin(),
					left_loss_values->end(), shared_ptr<longdouble>(new longdouble(0)),
					[&] (shared_ptr<longdouble> a, shared_ptr<longdouble> b)
					{ return shared_ptr<longdouble>(new longdouble(*a + *b)); });
	longdouble next_right_base_loss_value = *right_base_loss_value;

	shared_ptr<P> added_right_partial_solution =
			PartialSolution::construct(shared_ptr<list<shared_ptr<SackItem>>>(new
					list<shared_ptr<SackItem>>()),
					split_sack_item, break_partial_solution,
					next_right_base_loss_value, shared_ptr<list<shared_ptr<P>>>(new
							list<shared_ptr<P>>()));

	shared_ptr<list<shared_ptr<P>>> next_right_winnowed_partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*right_winnowed_partial_solutions));
	next_right_winnowed_partial_solutions->push_front(added_right_partial_solution);

	// cout << endl;

	/*

	cout << "next left winnowed partial solutions:" << endl;

	for_each(next_left_winnowed_partial_solutions->begin(),
			next_left_winnowed_partial_solutions->end(),
			[&] (P *a) { cout << *(a->toString()) << endl; });

	*/

	// cout << endl;

	/*

	cout << "next right winnowed partial solutions:" << endl;

	for_each(next_right_winnowed_partial_solutions->begin(),
			next_right_winnowed_partial_solutions->end(),
			[&] (P *a) { cout << *(a->toString()) << endl; });

	*/

	// cout << endl;

	shared_ptr<P> result_partial_solution =
			this->combineSolutionsForLeftAndRight(next_left_winnowed_partial_solutions,
					next_right_winnowed_partial_solutions);

	// cout << *(result_partial_solution->toString()) << endl;

	return result_partial_solution;


}
shared_ptr<string> CoreSackSubproblem::toString() {
	shared_ptr<string> result_str = shared_ptr<string>(new string(""));
	shared_ptr<list<shared_ptr<SackItem>>> sack_items = this->getSackItems();
	for_each(sack_items->begin(), sack_items->end(),
			[&] (shared_ptr<SackItem> a)
			{ result_str = shared_ptr<string>(new
					string(*result_str + *(a->toString()) + " ")); });
	return result_str;
}

CoreSackSubproblem::CoreSackSubproblem(shared_ptr<SackProblem> source_problem,
		shared_ptr<list<shared_ptr<SackItem>>> sack_items, int capacity,
		shared_ptr<BreakPartialSolution> break_partial_solution)
		: SackSubproblem(source_problem, sack_items,
				capacity, break_partial_solution) {
	this->left_post_list_decompose_subproblem = NULL;
	this->right_post_list_decompose_subproblem = NULL;
	/*
	cout << "created a core sack problem with following items:" << endl;
	for_each(sack_items->begin(), sack_items->end(),
			[&] (SackItem *a) { cout << "core item: " << *(a->toString()) << endl; });
	*/
}

CoreSackSubproblem::~CoreSackSubproblem() {
	// cout << "destructing a core sack sub-problem" << endl;
	(this->left_post_list_decompose_subproblem).reset();
	(this->right_post_list_decompose_subproblem).reset();
}

// #include "PostListDecomposeSubproblem.hpp"

using P = PartialSolution;
// using L = list<PartialSolution>;
using NC = NonCoreSackSubproblem;
using G = IntegralityGapEstimate;
using A = PartialSolutionPathLabel;

int PostListDecomposeSubproblem::weightComp(shared_ptr<P> x, shared_ptr<P> y) {
	int weight_x = x->getTotalWeight();
	int weight_y = y->getTotalWeight();
	if (weight_x == weight_y) {
		return 0;
	} else if (weight_x > weight_y) {
		return 1;
	} else {
		// weight_x < weight_y
		return -1;
	}
}

shared_ptr<list<shared_ptr<P>>> PostListDecomposeSubproblem::
	mergeOnBasisOfWeight(shared_ptr<list<shared_ptr<P>>> partial_solutions1,
		shared_ptr<list<shared_ptr<P>>> partial_solutions2) {
	shared_ptr<list<shared_ptr<P>>> result =
			PostListDecomposeSubproblem::
			mergeOnBasisOfWeightHelper(partial_solutions1,
					partial_solutions2, shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>()));
	return result;
}

shared_ptr<list<shared_ptr<P>>> PostListDecomposeSubproblem::
	mergeOnBasisOfWeightHelper(shared_ptr<list<shared_ptr<P>>> partial_solutions1,
		shared_ptr<list<shared_ptr<P>>> partial_solutions2,
		shared_ptr<list<shared_ptr<P>>> merged_partial_solutions) {
	if (partial_solutions1->size() == 0 && partial_solutions2->size() == 0) {
		return merged_partial_solutions;
	} else if (partial_solutions1->size() == 0 && partial_solutions2->size() != 0) {
		shared_ptr<P> partial_solution2 = partial_solutions2->front();
		shared_ptr<list<shared_ptr<P>>> next_partial_solutions2 = partial_solutions2;
		next_partial_solutions2->pop_front();
		merged_partial_solutions->push_back(partial_solution2);
		return PostListDecomposeSubproblem::
				mergeOnBasisOfWeightHelper(partial_solutions1,
						next_partial_solutions2, merged_partial_solutions);
	} else if (partial_solutions1->size() != 0 && partial_solutions2->size() == 0) {
		shared_ptr<P> partial_solution1 = partial_solutions1->front();
		shared_ptr<list<shared_ptr<P>>> next_partial_solutions1 = partial_solutions1;
		next_partial_solutions1->pop_front();
		merged_partial_solutions->push_back(partial_solution1);
		return PostListDecomposeSubproblem::
				mergeOnBasisOfWeightHelper(next_partial_solutions1,
						partial_solutions2, merged_partial_solutions);
	} else {
		shared_ptr<P> partial_solution1 = partial_solutions1->front();
		shared_ptr<P> partial_solution2 = partial_solutions2->front();
		shared_ptr<P> chosen_partial_solution = NULL;
		shared_ptr<list<shared_ptr<P>>> next_partial_solution_list1 = partial_solutions1;
		shared_ptr<list<shared_ptr<P>>> next_partial_solution_list2 = partial_solutions2;
		int weight_comp_result = PostListDecomposeSubproblem::
				weightComp(partial_solution1, partial_solution2);
		if ((weight_comp_result == -1) || (weight_comp_result == 0)) {
			chosen_partial_solution = partial_solution1;
			next_partial_solution_list1->pop_front();
		} else if (weight_comp_result == 1) {
			chosen_partial_solution = partial_solution2;
			next_partial_solution_list2->pop_front();
		}
		merged_partial_solutions->push_back(chosen_partial_solution);
		return PostListDecomposeSubproblem::
				mergeOnBasisOfWeightHelper(next_partial_solution_list1,
						next_partial_solution_list2, merged_partial_solutions);
		}
	}

shared_ptr<list<shared_ptr<P>>> PostListDecomposeSubproblem::
	filterOnBasisOfDominateRelation(shared_ptr<list<shared_ptr<P>>> L_curr,
		shared_ptr<NC> non_core_subproblem) {
	// return L_curr;
	shared_ptr<Dictionary<int, P>> weight_to_partial_solution_list_dict =
			shared_ptr<Dictionary<int, P>>(new Dictionary<int, P>());
	for (shared_ptr<P> partial_solution : *L_curr) {
		shared_ptr<int> weight = shared_ptr<int>(new int(partial_solution->getTotalWeight()));
		weight_to_partial_solution_list_dict->insert(weight, partial_solution);
	}
	shared_ptr<list<shared_ptr<P>>> partial_solution_list =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	shared_ptr<list<shared_ptr<int>>> ordered_weight_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	ordered_weight_values->resize(L_curr->size(), NULL);
	transform(L_curr->begin(), L_curr->end(), ordered_weight_values->begin(),
			[&] (shared_ptr<P> a) { return shared_ptr<int>(new int(a->getTotalWeight())); });
	/*
	cout << "ordered weight values:" << endl;
	for_each(ordered_weight_values->begin(), ordered_weight_values->end(),
			[&] (int *a) { cout << to_string(*a) << endl; });
			*/
	shared_ptr<list<shared_ptr<int>>> distinct_ordered_weight_values =
			Util::removeDuplicateValuesGivenSortedValues(ordered_weight_values);
	/*
	cout << "distinct ordered weight values:" << endl;
	for_each(distinct_ordered_weight_values->begin(), distinct_ordered_weight_values->end(),
				[&] (int *a) { cout << to_string(*a) << endl; });
	*/
	for (shared_ptr<int> weight : *distinct_ordered_weight_values) {
		shared_ptr<list<shared_ptr<tuple<shared_ptr<int>, shared_ptr<P>>>>> weight_partial_solution_pairs =
				weight_to_partial_solution_list_dict->findAll(weight);
		shared_ptr<list<shared_ptr<P>>> curr_partial_solution_list =
				shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
		curr_partial_solution_list->resize(weight_partial_solution_pairs->size(), NULL);
		transform(weight_partial_solution_pairs->begin(),
				weight_partial_solution_pairs->end(),
				curr_partial_solution_list->begin(),
				[&] (shared_ptr<tuple<shared_ptr<int>, shared_ptr<P>>> a) { return get<1>(*a); });
		shared_ptr<list<shared_ptr<longlong>>> profit_values =
				shared_ptr<list<shared_ptr<longlong>>>(new list<shared_ptr<longlong>>());
		profit_values->resize(curr_partial_solution_list->size(), NULL);
		transform(curr_partial_solution_list->begin(),
				curr_partial_solution_list->end(),
				profit_values->begin(),
				[&] (shared_ptr<P> a) { return shared_ptr<longlong>(new longlong(a->getTotalProfit())); });
		shared_ptr<longlong>(max_profit_value) = accumulate(profit_values->begin(),
				profit_values->end(), shared_ptr<longlong>(new longlong(0)),
				[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
				{ return (*a > *b) ? shared_ptr<longlong>(new longlong(*a)) :
						shared_ptr<longlong>(new longlong(*b)); });
		longlong next_max_profit_value = *max_profit_value;
		shared_ptr<list<shared_ptr<P>>> candidate_partial_solutions =
				shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*curr_partial_solution_list));
		// cout << "# of current partial solutions: " << curr_partial_solution_list->size() << endl;
		// cout << "# of candidate partial solutions pre-winnow: " << candidate_partial_solutions->size() << endl;
		// susceptible to longlong overflow
		candidate_partial_solutions->
			erase(remove_if(candidate_partial_solutions->begin(),
				candidate_partial_solutions->end(),
				[&] (shared_ptr<P> a)
				{ longlong difference = abs(a->getTotalProfit() - next_max_profit_value);
				// cout << "profit difference: " << difference << endl;
				  return (difference < 0.001) == false; }),
					candidate_partial_solutions->end());
		shared_ptr<list<shared_ptr<A>>> path_labels =
				shared_ptr<list<shared_ptr<A>>>(new list<shared_ptr<A>>());
		// cout << "candidate partial_solutions:" << endl;
		/*
		for_each(candidate_partial_solutions->begin(),
				candidate_partial_solutions->end(),
				[&] (PartialSolution *a) { cout << *(a->toString()) << endl; });
		*/
		path_labels->resize(candidate_partial_solutions->size(), NULL);
		transform(candidate_partial_solutions->begin(),
				candidate_partial_solutions->end(),
				path_labels->begin(),
				[&] (shared_ptr<P> a)
				{ return a->toPartialSolutionPathLabel(); });
		shared_ptr<A> best_path_label = PartialSolutionPathLabel::getMin(path_labels);
		shared_ptr<list<shared_ptr<P>>> next_candidate_partial_solutions =
				shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*candidate_partial_solutions));
		// cout << "# of candidate partial solutions: " << candidate_partial_solutions->size() << endl;
		next_candidate_partial_solutions->
			erase(remove_if(next_candidate_partial_solutions->begin(),
					next_candidate_partial_solutions->end(),
					[&] (shared_ptr<P> a)
					{
			// cout << *(a->toExtendedString()) << endl;
			return (a->toPartialSolutionPathLabel()->
							isEqualTo(best_path_label)) == false; }),
					next_candidate_partial_solutions->end());
		// cout << "# of next candidate partial solutions: " << next_candidate_partial_solutions->size() << endl;
		shared_ptr<P> chosen_partial_solution = next_candidate_partial_solutions->front();
		partial_solution_list->push_back(chosen_partial_solution);
		/*
		partial_solution_list->splice(partial_solution_list->end(),
				*candidate_partial_solutions, candidate_partial_solutions->begin(),
				candidate_partial_solutions->end());
		*/
	}
	shared_ptr<list<shared_ptr<P>>> next_L_curr =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*partial_solution_list));
	longlong best_profit = 0;
	shared_ptr<list<shared_ptr<P>>> partial_solutions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	for (shared_ptr<P> partial_solution : *next_L_curr) {
		longlong curr_profit = partial_solution->getTotalProfit();
		int curr_weight = partial_solution->getTotalWeight();
		if (curr_profit >= best_profit) {
			partial_solutions->push_back(partial_solution);
		}
		best_profit = max(best_profit, curr_profit);
	}
	shared_ptr<list<shared_ptr<P>>> next_next_L_curr =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*partial_solutions));
	return next_next_L_curr;
}

shared_ptr<list<shared_ptr<P>>> PostListDecomposeSubproblem::
	filterOnBasisOfLossValue(shared_ptr<list<shared_ptr<P>>> L_curr,
		shared_ptr<G> integrality_gap_estimate, shared_ptr<SackItem> sack_item,
		shared_ptr<SackItem> split_sack_item) {

	shared_ptr<list<shared_ptr<P>>> L_next =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*L_curr));
	L_next->erase(remove_if(L_next->begin(), L_next->end(),
			[&] (shared_ptr<P> a) { return (a->getTotalLossValue() <=
				(integrality_gap_estimate->getValue() + 0.001))
				== false; }), L_next->end());
	return L_next;
}

void PostListDecomposeSubproblem::
	_setCurrentWinnowedParetoPointsUsingStarterPartialSolution() {
	shared_ptr<CoreSackSubproblem> core_subproblem =
			static_pointer_cast<CoreSackSubproblem>(this->getSourceProblem());
	bool is_left_portion = this->is_left_portion;
	shared_ptr<PostListDecomposeSubproblem> next_this =
			static_pointer_cast<PostListDecomposeSubproblem>(shared_from_this());
	shared_ptr<P> starter_partial_solution =
			core_subproblem->getPostListDecomposeSubproblemStarterPartialSolution(next_this,
					is_left_portion);
	shared_ptr<list<shared_ptr<P>>> L_curr =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	L_curr->push_back(starter_partial_solution);
	this->_setCurrentWinnowedParetoPoints(L_curr);
}

shared_ptr<list<shared_ptr<P>>> PostListDecomposeSubproblem::
	_getCurrentWinnowedParetoPoints() {
	return this->L_curr;
}

void PostListDecomposeSubproblem::
	_setCurrentWinnowedParetoPoints(shared_ptr<list<shared_ptr<P>>> L_curr) {
	this->L_curr = L_curr;
}

void PostListDecomposeSubproblem::
	iterateSolve(shared_ptr<SackItem> curr_sack_item,
	shared_ptr<G> integrality_gap_estimate, shared_ptr<NC> non_core_subproblem) {
	int capacity = this->getCapacity();
	shared_ptr<list<shared_ptr<P>>> L_curr = this->_getCurrentWinnowedParetoPoints();
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<list<shared_ptr<P>>> L_additions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>());
	L_additions->resize(L_curr->size(), NULL);
	transform(L_curr->begin(), L_curr->end(),
			L_additions->begin(),
			[&] (shared_ptr<P> a) { return a->clone(break_partial_solution); });
	shared_ptr<bool> weights_increase = NULL;
	/*
	cout << "current post-list-decomposition problem is left portion: " + to_string(this->is_left_portion) << endl;
	cout << "break partial solution: " + *(break_partial_solution->toString()) << endl;
	cout << "CONSIDERING ITEM: " + *(curr_sack_item->toString()) + "\n";
	*/
	if (break_partial_solution->hasSackItem(curr_sack_item) == true) {
		// cout << "undo adding a sack item" << endl;
		weights_increase = shared_ptr<bool>(new bool(false));
		for (shared_ptr<P> partial_solution :  *L_additions) {
			partial_solution->undoAddSackItem(curr_sack_item);
		}
	} else if (break_partial_solution->hasSackItem(curr_sack_item) == false) {
		// cout << "adding a sack item" << endl;
		weights_increase = shared_ptr<bool>(new bool(true));
		for (shared_ptr<P> partial_solution : *L_additions) {
			partial_solution->addSackItem(curr_sack_item, break_partial_solution);
		}
	}
	shared_ptr<list<shared_ptr<P>>> next_L_additions =
			shared_ptr<list<shared_ptr<P>>>(new list<shared_ptr<P>>(*L_additions));
	next_L_additions->erase(remove_if(next_L_additions->begin(),
			next_L_additions->end(), [&] (shared_ptr<P> a)
			{ return (a->isFeasible(capacity) == true) == false; }),
			next_L_additions->end());
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	shared_ptr<list<shared_ptr<P>>> L_next = NULL;
	bool next_weights_increase = *weights_increase;
	if (next_weights_increase == true) {
		L_next = PostListDecomposeSubproblem::
				mergeOnBasisOfWeight(L_curr, next_L_additions);
	} else if (next_weights_increase == false) {
		L_next = PostListDecomposeSubproblem::
				mergeOnBasisOfWeight(next_L_additions, L_curr);
	}

	L_next = PostListDecomposeSubproblem::
			filterOnBasisOfDominateRelation(L_next, non_core_subproblem);
	L_next = PostListDecomposeSubproblem::
			filterOnBasisOfLossValue(L_next,
					integrality_gap_estimate, curr_sack_item, split_sack_item);
	this->_setCurrentWinnowedParetoPoints(L_next);
	}

bool PostListDecomposeSubproblem::getIsLeftPortion() {
	return this->is_left_portion;
}

void PostListDecomposeSubproblem::
	addItemBasedOnIsStarterItemAndLossValue(shared_ptr<SackItem> sack_item) {
	shared_ptr<BreakPartialSolution> break_partial_solution = this->_getBreakPartialSolution();
	bool is_a_break_sack_item = break_partial_solution->hasSackItem(sack_item);
	if (is_a_break_sack_item == true) {
		(this->remaining_break_sack_items)->push_back(sack_item);
	} else {
		(this->remaining_non_break_sack_items)->push_back(sack_item);
	}
}

shared_ptr<SackItem> PostListDecomposeSubproblem::
	getNextRemainingItemBasedOnIsStarterItemAndLossValue() {
	shared_ptr<list<shared_ptr<SackItem>>> remaining_break_sack_items =
			this->remaining_break_sack_items;
	shared_ptr<list<shared_ptr<SackItem>>> remaining_non_break_sack_items =
			this->remaining_non_break_sack_items;
	if (remaining_break_sack_items->size() != 0) {
		shared_ptr<SackItem> next_sack_item = remaining_break_sack_items->front();
		return next_sack_item;
	} else {
		shared_ptr<SackItem> next_sack_item = remaining_non_break_sack_items->front();
		return next_sack_item;
	}
}

void PostListDecomposeSubproblem::
	removeNextRemainingItemBasedOnIsStarterItemAndLossValue() {
	shared_ptr<list<shared_ptr<SackItem>>> remaining_break_sack_items =
			this->remaining_break_sack_items;
	shared_ptr<list<shared_ptr<SackItem>>> remaining_non_break_sack_items =
			this->remaining_non_break_sack_items;
	if (remaining_break_sack_items->size() != 0) {
		remaining_break_sack_items->pop_front();
	} else {
		remaining_non_break_sack_items->pop_front();
	}
}

bool PostListDecomposeSubproblem::isFinished() {
	bool have_remaining_break_sack_items =
			(this->remaining_break_sack_items)->size() != 0;
	bool have_remaining_non_break_sack_items =
			(this->remaining_non_break_sack_items)->size() != 0;
	bool have_remaining_sack_items =
			(have_remaining_break_sack_items == true) ||
			(have_remaining_non_break_sack_items == true);
	bool is_finished = have_remaining_sack_items == false;
	return is_finished;
}

void PostListDecomposeSubproblem::init() {
	// important to have; otherwise unusual behavior may result
	SackProblem::init();
	this->_setCurrentWinnowedParetoPointsUsingStarterPartialSolution();
}

PostListDecomposeSubproblem::
	PostListDecomposeSubproblem(shared_ptr<SackProblem> source_problem,
			shared_ptr<list<shared_ptr<SackItem>>> sack_items, int capacity,
			shared_ptr<BreakPartialSolution> break_partial_solution,
			bool is_left_portion) : SackSubproblem(source_problem,
					sack_items, capacity, break_partial_solution) {
	this->is_left_portion = is_left_portion;
	shared_ptr<list<shared_ptr<SackItem>>> remaining_break_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items));
	shared_ptr<list<shared_ptr<SackItem>>> remaining_non_break_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sack_items));
	// remaining_break_sack_items->resize(sack_items->size(), NULL);
	remaining_break_sack_items->erase(remove_if(remaining_break_sack_items->begin(),
			remaining_break_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return break_partial_solution->hasSackItem(a) == false; }),
			remaining_break_sack_items->end());
	// remaining_non_break_sack_items->resize(sack_items->size(), NULL);
	remaining_non_break_sack_items->erase(remove_if(remaining_non_break_sack_items->begin(),
			remaining_non_break_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return (break_partial_solution->hasSackItem(a) == false) == false; }),
			remaining_non_break_sack_items->end());
	this->remaining_break_sack_items = remaining_break_sack_items;
	this->remaining_non_break_sack_items = remaining_non_break_sack_items;


}

PostListDecomposeSubproblem::~PostListDecomposeSubproblem() {
	// cout << "destructing a post-list-decompose sub-problem" << endl;
	// cout << "remaining break sack item collection use count: " << (this->remaining_break_sack_items).use_count() << endl;
	// cout << "current partial solution collection use count: " << (this->L_curr).use_count() << endl;
	(this->remaining_break_sack_items).reset();
	(this->remaining_non_break_sack_items).reset();
	(this->L_curr).reset();
}

// #include "OriginalSackProblem.hpp"

// #include "SackProblem.hpp"

// #include "../feed_optimizer/Solution.t.hpp"

using C = CoreSackSubproblem;
using D = NonCoreSackSubproblem;


using D = NonCoreSackSubproblem;

using G = IntegralityGapEstimate;

void OriginalSackProblem::
	moveItemFromNonCoreToCore(shared_ptr<C> core_subproblem, shared_ptr<D> non_core_subproblem,
	shared_ptr<BreakPartialSolution> break_partial_solution, shared_ptr<SackItem> split_sack_item) {
	/*
	cout << "pre-move current core items:" << endl;
	list<SackItem *> *core_sack_items = core_subproblem->getSackItems();
	for_each(core_sack_items->begin(), core_sack_items->end(),
			[&] (SackItem *a) { cout << "core item: " << *(a->toString()) << endl; });
	cout << "pre-move current non-core items:" << endl;
	list<SackItem *> *non_core_sack_items = non_core_subproblem->getSackItems();
	for_each(non_core_sack_items->begin(), non_core_sack_items->end(),
			[&] (SackItem *a) { cout << "non-core item: " << *(a->toString()) << endl; });
	*/
	shared_ptr<SackItem> chosen_item =
			non_core_subproblem->getSackItemWithLowestLossValue();
	// cout << chosen_item->getLossValue(split_sack_item, true) << endl;
	core_subproblem->addSackItemWithLargeLossValue(chosen_item);
	non_core_subproblem->removeSackItemWithLowestLossValue();
	/*
	cout << "post-move current core items:" << endl;
	list<SackItem *> *next_core_sack_items = core_subproblem->getSackItems();
	for_each(next_core_sack_items->begin(), next_core_sack_items->end(),
			[&] (SackItem *a) { cout << "core item: " << *(a->toString()) << endl; });
	cout << "post-move current non-core items:" << endl;
	list<SackItem *> *next_non_core_sack_items = non_core_subproblem->getSackItems();
	for_each(next_non_core_sack_items->begin(), next_non_core_sack_items->end(),
			[&] (SackItem *a) { cout << "non-core item: " << *(a->toString()) << endl; });
	*/

	// cout << "moving item: " << *(chosen_item->toString()) << endl;

	int chosen_item_weight = chosen_item->getWeight();
	int core_subproblem_capacity = core_subproblem->getCapacity();
	// cout << chosen_item_weight << endl;
	int non_core_subproblem_capacity = non_core_subproblem->getCapacity();
	bool is_part_of_break_solution = break_partial_solution->hasSackItem(chosen_item);
	shared_ptr<int> next_core_subproblem_capacity = NULL;
	shared_ptr<int> next_non_core_subproblem_capacity = NULL;
if (is_part_of_break_solution == true) {
	next_core_subproblem_capacity =
			shared_ptr<int>(new int(core_subproblem_capacity + chosen_item_weight));
	next_non_core_subproblem_capacity =
			shared_ptr<int>(new int(non_core_subproblem_capacity - chosen_item_weight));
	// cout << *next_core_subproblem_capacity << endl;
	// cout << *next_non_core_subproblem_capacity << endl;
} else {
	next_core_subproblem_capacity = shared_ptr<int>(new int(core_subproblem_capacity));
	next_non_core_subproblem_capacity = shared_ptr<int>(new int(non_core_subproblem_capacity));
}
core_subproblem->setCapacity(*next_core_subproblem_capacity);
non_core_subproblem->setCapacity(*next_non_core_subproblem_capacity);
}

void OriginalSackProblem::
	ponder(int n) {

}

shared_ptr<C> OriginalSackProblem::
	getCoreSubproblem() {
	return this->core_subproblem;

}

shared_ptr<D> OriginalSackProblem::
	getNonCoreSubproblem() {
	return this->non_core_subproblem;
}

void OriginalSackProblem::
	setCoreSubproblem(shared_ptr<C> core_subproblem) {
	this->core_subproblem = core_subproblem;
}

void OriginalSackProblem::
	setNonCoreSubproblem(shared_ptr<D> non_core_subproblem) {
	this->non_core_subproblem = non_core_subproblem;
}

shared_ptr<list<shared_ptr<SackItem>>> OriginalSackProblem::
	_getCoreSackItems(longdouble cutoff_loss_value) {
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items = this->_getItemsSortedByLossValue();
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	shared_ptr<list<shared_ptr<SackItem>>> culled_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sorted_sack_items));
	culled_sack_items->erase(remove_if(culled_sack_items->begin(),
			culled_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return (a->getLossValue(split_sack_item, true)
					<= cutoff_loss_value) == false; }),
			culled_sack_items->end());
	return culled_sack_items;
}

shared_ptr<list<shared_ptr<SackItem>>> OriginalSackProblem::
	_getNonCoreSackItems(longdouble cutoff_loss_value) {
	shared_ptr<list<shared_ptr<SackItem>>> sorted_sack_items = this->_getItemsSortedByLossValue();
	shared_ptr<SackItem> split_sack_item = this->_getSplitSackItem();
	shared_ptr<list<shared_ptr<SackItem>>> culled_sack_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*sorted_sack_items));
	// cout << "sorted sack items:" << endl;
	/*
	for_each(sorted_sack_items->begin(), sorted_sack_items->end(),
			[&] (SackItem *a) { cout << a->getLossValue(split_sack_item, true) << endl; });
	*/
	culled_sack_items->erase(remove_if(culled_sack_items->begin(),
			culled_sack_items->end(),
			[&] (shared_ptr<SackItem> a) { return ((a->getLossValue(split_sack_item, true)
					<= cutoff_loss_value) == false) == false; }),
			culled_sack_items->end());
	// cout << cutoff_loss_value << endl;
	return culled_sack_items;
}

shared_ptr<list<shared_ptr<SackItem>>> OriginalSackProblem::
	_getNonCoreIncludedItems(longdouble cutoff_loss_value) {
	shared_ptr<list<shared_ptr<SackItem>>> non_core_sack_items =
			this->_getNonCoreSackItems(cutoff_loss_value);
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<list<shared_ptr<SackItem>>> winnowed_items =
			shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*non_core_sack_items));
	winnowed_items->erase(remove_if(winnowed_items->begin(), winnowed_items->end(),
			[&] (shared_ptr<SackItem> a) { return break_partial_solution->hasSackItem(a) == false; }),
			winnowed_items->end());
	return winnowed_items;
}

int OriginalSackProblem::
	_getNonCoreIncludedItemTotalWeight(longdouble cutoff_loss_value) {
	shared_ptr<list<shared_ptr<SackItem>>> non_core_included_items =
			this->_getNonCoreIncludedItems(cutoff_loss_value);
	shared_ptr<list<shared_ptr<int>>> weight_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	weight_values->resize(non_core_included_items->size(), NULL);
	transform(non_core_included_items->begin(),
			non_core_included_items->end(),
			weight_values->begin(),
			[&] (shared_ptr<SackItem> a) { return shared_ptr<int>(new int(a->getWeight())); });
	shared_ptr<int> total_weight = accumulate(weight_values->begin(),
			weight_values->end(), shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	int next_total_weight = *total_weight;
	return next_total_weight;
}

shared_ptr<C> OriginalSackProblem::
	_getCoreSubproblem(longdouble cutoff_loss_value) {
	shared_ptr<list<shared_ptr<SackItem>>> core_sack_items =
			this->_getCoreSackItems(cutoff_loss_value);
	shared_ptr<OriginalSackProblem> source_problem =
			static_pointer_cast<OriginalSackProblem>(shared_from_this());
	int capacity = this->getCapacity();
	int non_core_included_item_total_weight =
			this->_getNonCoreIncludedItemTotalWeight(cutoff_loss_value);
	int core_capacity = capacity - non_core_included_item_total_weight;
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<CoreSackSubproblem> core_problem =
			shared_ptr<CoreSackSubproblem>(new CoreSackSubproblem(source_problem,
					core_sack_items, core_capacity, break_partial_solution));
	core_problem->init();
	return core_problem;
}

shared_ptr<D> OriginalSackProblem::
	_getNonCoreSubproblem(longdouble cutoff_loss_value) {
	shared_ptr<list<shared_ptr<SackItem>>> non_core_sack_items =
			this->_getNonCoreSackItems(cutoff_loss_value);
	shared_ptr<OriginalSackProblem> source_problem =
			static_pointer_cast<OriginalSackProblem>(shared_from_this());
	int capacity = this->getCapacity();
	int non_core_included_item_total_weight =
			this->_getNonCoreIncludedItemTotalWeight(cutoff_loss_value);
	int non_core_capacity = non_core_included_item_total_weight;
	shared_ptr<BreakPartialSolution> break_partial_solution =
			this->_getBreakPartialSolution();
	shared_ptr<NonCoreSackSubproblem> non_core_problem =
			shared_ptr<NonCoreSackSubproblem>(new NonCoreSackSubproblem(source_problem,
					non_core_sack_items, non_core_capacity, break_partial_solution));
	non_core_problem->init();
	return non_core_problem;
}

shared_ptr<tuple<shared_ptr<C>, shared_ptr<D>>> OriginalSackProblem::
	divideIntoCoreAndNonCore(longdouble cutoff_loss_value) {
	shared_ptr<C> core_subproblem = this->_getCoreSubproblem(cutoff_loss_value);
	// cout << "core subproblem use count: " << core_subproblem.use_count() << endl;
	shared_ptr<D> non_core_subproblem = this->_getNonCoreSubproblem(cutoff_loss_value);
	this->setCoreSubproblem(core_subproblem);
	// cout << "next core subproblem use count: " << core_subproblem.use_count() << endl;
	this->setNonCoreSubproblem(non_core_subproblem);
	auto tuple_result = new tuple<shared_ptr<C>, shared_ptr<D>>(core_subproblem, non_core_subproblem);
	auto result = shared_ptr<tuple<shared_ptr<C>, shared_ptr<D>>>(tuple_result);
	// cout << "next next core subproblem use count: " << core_subproblem.use_count() << endl;
	core_subproblem.reset();
	non_core_subproblem.reset();
	return result;
	/*
	shared_ptr<tuple<shared_ptr<C>, shared_ptr<D>>> result =
			make_shared<tuple<shared_ptr<C>, shared_ptr<D>>>(*(new tuple<shared_ptr<C>,
					shared_ptr<D>>(core_subproblem, non_core_subproblem)));
	*/
	// cout << "divided into core and non-core" << endl;
	// cout << "core subproblem: " + *(core_subproblem->toString()) << endl;
	// cout << "non-core subproblem: " + *(non_core_subproblem->toString()) << endl;
	/*
	core_subproblem.reset();
	non_core_subproblem.reset();
	*/
	return result;
}

bool OriginalSackProblem::
	canStopExpandingCoreSubproblem(shared_ptr<C> core_subproblem,
		shared_ptr<D> non_core_subproblem, shared_ptr<G> integrality_gap_estimate) {
	shared_ptr<SackItem> split_sack_item = core_subproblem->_getSplitSackItem();
	bool non_core_subproblem_has_no_items = non_core_subproblem->getNumSackItems() == 0;
	// cout << non_core_subproblem_has_no_items << endl;
	if (non_core_subproblem_has_no_items == true) {
		bool can_stop_expanding = true;
		return can_stop_expanding;
	} else {
		shared_ptr<SackItem> item_with_next_loss_value = non_core_subproblem->getItemWithLowestLossValue();
		longdouble next_loss_value = item_with_next_loss_value->getLossValue(split_sack_item, true);
		longdouble integrality_gap_estimate_value = integrality_gap_estimate->getValue();
		bool can_stop_expanding = next_loss_value > (integrality_gap_estimate_value + 0.0001);
		return can_stop_expanding;
	}
}

shared_ptr<list<shared_ptr<SackItem>>> OriginalSackProblem::solve() {
	shared_ptr<list<shared_ptr<SackItem>>> items = this->getSackItems();
	// cout << "items:" << endl;
	/*
	for_each(items->begin(), items->end(),
			[&] (SackItem *a) { cout << *(a->toString()) << endl; });
	*/
	int n = items->size();
	int W = this->getCapacity();
	// cout << "number of items: " + to_string(n) << endl;
	// cout << "capacity: " + to_string(W) << endl;
	shared_ptr<list<shared_ptr<longlong>>> profit_values =
			shared_ptr<list<shared_ptr<longlong>>>(new list<shared_ptr<longlong>>());
	profit_values->resize(items->size(), NULL);
	transform(items->begin(), items->end(), profit_values->begin(),
			[&] (shared_ptr<SackItem> a) { return shared_ptr<longlong>(new longlong(a->getProfit())); });
	shared_ptr<list<shared_ptr<int>>> weight_values =
			shared_ptr<list<shared_ptr<int>>>(new list<shared_ptr<int>>());
	weight_values->resize(items->size(), NULL);
	transform(items->begin(), items->end(), weight_values->begin(),
			[&] (shared_ptr<SackItem> a) { return shared_ptr<int>(new int(a->getWeight())); });
	shared_ptr<longlong> R_profit = accumulate(profit_values->begin(), profit_values->end(),
			shared_ptr<longlong>(new longlong(0)),
			[&] (shared_ptr<longlong> a, shared_ptr<longlong> b)
			{ return (*a > *b) ? shared_ptr<longlong>(new longlong(*a)) : shared_ptr<longlong>(new longlong(*b)); });
	shared_ptr<int> R_weight = accumulate(weight_values->begin(), weight_values->end(),
			shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return (*a > *b) ? shared_ptr<int>(new int(*a)) : shared_ptr<int>(new int(*b)); });
	shared_ptr<int> total_weight = accumulate(weight_values->begin(), weight_values->end(),
			shared_ptr<int>(new int(0)),
			[&] (shared_ptr<int> a, shared_ptr<int> b)
			{ return shared_ptr<int>(new int(*a + *b)); });
	longlong next_R_profit = *R_profit;
	int next_R_weight = *R_weight;
	int next_total_weight = *total_weight;
	if (next_total_weight <= W) {
shared_ptr<list<shared_ptr<SackItem>>> chosen_items =
		shared_ptr<list<shared_ptr<SackItem>>>(new list<shared_ptr<SackItem>>(*items));
return chosen_items;
	} else {
		shared_ptr<tuple<shared_ptr<list<shared_ptr<SackItem>>>,
		shared_ptr<SackItem>, shared_ptr<longdouble>>> result =
				FractionalKnapsack::linearTimeFractionalSolve(items, W);
		shared_ptr<list<shared_ptr<SackItem>>> break_partial_solution_sack_items;
		shared_ptr<SackItem> split_sack_item;
		shared_ptr<longdouble> split_item_fraction;
tie(break_partial_solution_sack_items, split_sack_item, split_item_fraction) = *result;
shared_ptr<BreakPartialSolution> break_partial_solution =
		BreakPartialSolution::construct(break_partial_solution_sack_items, split_sack_item);
longdouble next_split_item_fraction = *split_item_fraction;
shared_ptr<tuple<shared_ptr<longdouble>, shared_ptr<longdouble>>> fractional_solution_profit_weight_tuple =
		FractionalKnapsack::toFractionalSolutionProfitAndWeightTuple(break_partial_solution,
				split_sack_item, next_split_item_fraction);
shared_ptr<longdouble> fractional_solution_profit;
shared_ptr<longdouble> fractional_solution_weight;
tie(fractional_solution_profit, fractional_solution_weight) = *fractional_solution_profit_weight_tuple;
longdouble next_fractional_solution_profit = *fractional_solution_profit;
longdouble next_fractional_solution_weight = *fractional_solution_weight;

// cout << split_sack_item->getLossValue(split_sack_item, true) << endl;

// cout << *(split_sack_item->toString()) << endl;

// cout << next_fractional_solution_profit << " " << next_fractional_solution_weight << endl;
/*
cout << "fractional solution profit and weight: ";
cout << "(" + to_string(next_fractional_solution_profit);
cout << ", ";
cout << to_string(next_fractional_solution_weight) + ")";
cout << endl;
*/
longdouble gamma_est = 0.730079606 * (pow(log(n), 2.0) / (1.0 * n)) + 0.000013577;
// cout << "gamma value estimate: " + to_string(gamma_est) << endl;
longdouble cutoff_loss_value = gamma_est * next_R_profit;
// cout << "cut-off loss value: " + to_string(cutoff_loss_value) << endl;
shared_ptr<G> integrality_gap_estimate = shared_ptr<IntegralityGapEstimate>(new IntegralityGapEstimate(next_fractional_solution_profit, 0));
longlong break_partial_solution_profit = break_partial_solution->getTotalProfit();
// cout << break_partial_solution_profit << endl;
// might be risky
// integrality_gap_estimate->updateBestIntegerSolutionProfit(break_partial_solution_profit - 1);
shared_ptr<C> core_subproblem;
shared_ptr<D> non_core_subproblem;
shared_ptr<tuple<shared_ptr<C>, shared_ptr<D>>> next_result =
		this->divideIntoCoreAndNonCore(cutoff_loss_value * 1.0);
tie(core_subproblem, non_core_subproblem) = *next_result;
get<0>(*next_result).reset();
get<1>(*next_result).reset();
shared_ptr<P> non_core_subproblem_partial_solution = non_core_subproblem->solve();
longlong non_core_subproblem_partial_solution_profit =
		non_core_subproblem_partial_solution->getTotalProfit();
// cout << "pre-solve core subproblem sack items: " + *(core_subproblem->toString()) << endl;
shared_ptr<P> core_subproblem_partial_solution =
		core_subproblem->solve(integrality_gap_estimate, non_core_subproblem_partial_solution_profit);
// cout << "post-solve core subproblem sack items: " + *(core_subproblem->toString()) << endl;
longlong core_subproblem_partial_solution_profit =
		core_subproblem_partial_solution->getTotalProfit();
longlong combined_profit = core_subproblem_partial_solution_profit +
		non_core_subproblem_partial_solution_profit;
// cout << core_subproblem_partial_solution_profit << endl;
// cout << non_core_subproblem_partial_solution_profit << endl;
// cout << combined_profit << endl;
integrality_gap_estimate->updateBestIntegerSolutionProfit(combined_profit);
while (this->canStopExpandingCoreSubproblem(core_subproblem, non_core_subproblem, integrality_gap_estimate) == false) {
// cout << "expanding core by one item" << endl;
OriginalSackProblem::moveItemFromNonCoreToCore(core_subproblem, non_core_subproblem, break_partial_solution, split_sack_item);
core_subproblem->getLeftPostListDecomposeSubproblem()->_setCurrentWinnowedParetoPointsUsingStarterPartialSolution();
core_subproblem->getRightPostListDecomposeSubproblem()->_setCurrentWinnowedParetoPointsUsingStarterPartialSolution();
non_core_subproblem_partial_solution = non_core_subproblem->solve();
non_core_subproblem_partial_solution_profit = non_core_subproblem_partial_solution->getTotalProfit();
core_subproblem_partial_solution = core_subproblem->solve(integrality_gap_estimate, non_core_subproblem_partial_solution_profit);
}
/*
cout << "core items: " << *(core_subproblem_partial_solution->toExtendedString()) << endl;
list<SackItem *> *core_subproblem_sack_items = core_subproblem->getSackItems();
for_each(core_subproblem_sack_items->begin(),
		core_subproblem_sack_items->end(),
		[&] (SackItem *a) { cout << "core sack item: " << *(a->toString()) << endl; });
cout << "non-core items: " << *(non_core_subproblem_partial_solution->toExtendedString()) << endl;
*/
shared_ptr<P> partial_solution =
		PartialSolution::
		_combinePartialSolutions(core_subproblem_partial_solution,
				non_core_subproblem_partial_solution, split_sack_item,
				this->_getBreakPartialSolution(), core_subproblem,
				non_core_subproblem);

shared_ptr<list<shared_ptr<SackItem>>> sack_items = partial_solution->getSackItems();
// cout << "post-solve core subproblem use count: " << core_subproblem.use_count() << endl;
// unnecessary
core_subproblem.reset();
non_core_subproblem.reset();
return sack_items;


	}
	}

OriginalSackProblem::OriginalSackProblem(shared_ptr<list<shared_ptr<SackItem>>> sack_items,
		int capacity, shared_ptr<BreakPartialSolution> break_partial_solution)
	: SackProblem(sack_items, capacity, break_partial_solution) {
	this->core_subproblem = NULL;
	this->non_core_subproblem = NULL;
}

OriginalSackProblem::~OriginalSackProblem() {
	// cout << "destructing an original sack problem" << endl;
	// cout << (this->core_subproblem).use_count() << endl;
	(this->core_subproblem).reset();
	(this->non_core_subproblem).reset();
}

#include <iostream>

#include <list>

#include <cstdlib>

#include <map>

#include <string>

#include <fstream>

#include <sstream>

// #include "/home/brianl/gperftools-2.4/src/gperftools/heap-profiler.h"

/*

extern "C" void HeapProfilerStart(const char *prefix);

std::string prefix = "hello";

HeapProfilerStart(prefix.c_str());

*/

/*

#include "../knapsack/FractionalKnapsack.hpp"
#include "../knapsack/PartialSolution.hpp"
#include "../util/Util.hpp"
#include "FeedOptimizer.hpp"

*/
/*

#include "../tree/binary_tree/BinaryTree.t.hpp"

#include "../tree/bst/BinarySearchTree.t.hpp"

#include "../tree/location_aware_bst/LocationAwareBinarySearchTree.t.hpp"

#include "../tree/ordered_bst/OrderedBinarySearchTree.t.hpp"

#include "../tree/bbst/SplayTree.t.hpp"

*/

/*

#include "../dictionary/Dictionary.t.hpp"

#include "../list/DoublyLinkedList.t.hpp"

#include "../event_queue/EventPriorityQueue.hpp"

#include "../knapsack/IdentifierOrderedSackItemTree.t.hpp"

*/

// #include "../util/Util.hpp"

/*

#include "../knapsack/SackItem.hpp"

#include "../knapsack/FractionalKnapsack.hpp"

#include "../knapsack/ListDecomposition.hpp"

*/

/*

#include "events/ItemTimeSpanningEvent.hpp"

#include "events/SolveEvent.hpp"

#include "events/ItemIntroduceEvent.hpp"

#include "events/ItemExpireEvent.hpp"

*/

// #include "../tree/bst/BinarySearchTree.t.hpp"

// using namespace std;
	//
int main() {

	// istream *infile = &cin;

	// istream *infile = &cin;

	// istream *infile = new ifstream("src/tests/official/input00.txt");

	// istream *infile = new ifstream("src/tests/test1.txt");

	// istream *infile = new ifstream("src/tests/test2.txt");

	// istream *infile = new ifstream("src/tests/test21.txt");

	// istream *infile = new ifstream("src/tests/test22.txt");

	// istream *infile = new ifstream("src/tests/test23.txt");

	// istream *infile = new ifstream("src/tests/test24.txt");

	// istream *infile = new ifstream("src/tests/test25.txt");

	shared_ptr<FeedItem> item1 = shared_ptr<FeedItem>(new FeedItem(50, 30, 1));

	shared_ptr<FeedItem> item2 = shared_ptr<FeedItem>(new FeedItem(40, 20, 2));

	shared_ptr<FeedItem> item3 = shared_ptr<FeedItem>(new FeedItem(45, 40, 3));

	shared_ptr<FeedItem> item4 = shared_ptr<FeedItem>(new FeedItem(45, 20, 4));

	shared_ptr<Dictionary<int, FeedItem>> curr_item_collection =
			shared_ptr<Dictionary<int, FeedItem>>(new Dictionary<int, FeedItem>());

	curr_item_collection->insert(shared_ptr<int>(new int(1)), item1);

	curr_item_collection->insert(shared_ptr<int>(new int(2)), item2);

	curr_item_collection->insert(shared_ptr<int>(new int(3)), item3);

	curr_item_collection->insert(shared_ptr<int>(new int(4)), item4);

	SolveEvent *solve_event = new SolveEvent(0, 100);

	solve_event->handle(curr_item_collection);

	return 0;

}


