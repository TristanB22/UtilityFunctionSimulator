# Agent.py
# Author: Tristan Brigham
# Enhanced cognitive agent with memory, reflection, planning, and goal-setting capabilities
# Based on generative agents architecture with comprehensive cognitive modules

# import the necessary libraries
import sys
import os
import datetime
from typing import Dict, Any, Optional, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Labor import Labor
from Agent.L2_data_object import L2_Data_Object

# Import cognitive architecture components
from Agent.memory_structures import MemoryRecord, MemoryStore, ReflectionMemory
from Agent.cognitive_modules import (
    perceive_environment, create_memory_from_observation,
    retrieve_relevant_memories, create_daily_plan, create_weekly_plan,
    plan_next_action, execute_action, daily_reflection, create_insight
)


class Agent:
    """
    A sophisticated cognitive agent with memory, reflection, planning, and goal-setting capabilities.
    Integrates multiple cognitive modules for human-like reasoning and behavior.
    """
    
    def __init__(self, 
                id: int, 
                name: str = None, 
                attributes: dict = None, 
                abilities: dict = None, 
                constraints: dict = None,
                l2_object: L2_Data_Object = None,
                ):
        """
        Initialize a cognitive agent with comprehensive mental architecture.

        Args:
            id (int): Unique identifier for the agent
            name (str): The name of the agent.
            attributes (dict): A dictionary of attributes of the agent.
            abilities (dict): A dictionary of abilities of the agent.
            constraints (dict): A dictionary of constraints of the agent.
            l2_object (L2_Data_Object): An L2_Data_Object instance containing the agent's data.
        """

        # Basic identity and attributes
        self.id = id
        self.name = name or f"Agent_{id}"
        self.attributes = attributes or {}
        self.abilities = abilities or {}
        self.constraints = constraints or {}
        self.l2_object = l2_object

        # Cognitive architecture components
        self.memory_stream = MemoryStore(max_memories=10000)
        self.reflection_memory = ReflectionMemory(max_reflections=1000)
        
        # Current state
        self.current_location = "unknown"
        self.current_goal = None
        self.current_planned_action = None
        self.current_daily_plan = None
        self.current_weekly_plan = None
        self.mood = "neutral"
        
        # Timing and scheduling
        self.last_reflection_time = None
        self.last_planning_time = None
        self.last_action_time = None
        self.last_action = None
        self.last_action_success = True
        
        # Initialize with basic memories and goals from L2 data
        self._initialize_from_l2_data()
        
        # Set initial goals and principles
        self._set_initial_goals_and_principles()

    def _initialize_from_l2_data(self):
        """Initialize agent memories and characteristics from L2 voter data."""
        if not self.l2_object:
            return
        
        l2_data = self.l2_object.all_data()
        
        # Create initial memories from L2 demographic data
        demographic_info = []
        if 'AGE' in l2_data:
            demographic_info.append(f"I am {l2_data['AGE']} years old")
        if 'GENDER' in l2_data:
            demographic_info.append(f"I identify as {l2_data['GENDER']}")
        if 'EDUCATION' in l2_data:
            demographic_info.append(f"My education level is {l2_data['EDUCATION']}")
        if 'INCOME' in l2_data:
            demographic_info.append(f"My income level is {l2_data['INCOME']}")
        if 'PARTY' in l2_data:
            demographic_info.append(f"My political affiliation is {l2_data['PARTY']}")
        
        # Add demographic memories
        for info in demographic_info:
            memory = create_memory_from_observation(
                agent=self,
                observation=info,
                context="demographic_background",
                source="background_knowledge",
                manual_importance=6.0
            )
            self.memory_stream.add_memory(memory)

    def _set_initial_goals_and_principles(self):
        """Set initial goals and principles for the agent."""
        # Basic universal principles
        initial_principles = [
            "Treat others with respect and kindness",
            "Strive for personal growth and learning",
            "Make decisions that align with my values"
        ]
        
        # Basic life goals
        initial_goals = [
            "Maintain good relationships with family and friends",
            "Stay healthy and take care of myself",
            "Contribute positively to my community"
        ]
        
        # Add more specific goals based on L2 data if available
        if self.l2_object:
            l2_data = self.l2_object.all_data()
            
            # Add goals based on age
            if 'AGE' in l2_data:
                age = int(l2_data['AGE']) if str(l2_data['AGE']).isdigit() else 35
                if age < 30:
                    initial_goals.extend([
                        "Build my career and develop professional skills",
                        "Explore new experiences and opportunities"
                    ])
                elif age < 50:
                    initial_goals.extend([
                        "Advance in my career and achieve financial stability",
                        "Balance work and family responsibilities"
                    ])
                else:
                    initial_goals.extend([
                        "Share my experience and mentor others",
                        "Focus on long-term health and retirement planning"
                    ])
            
            # Add goals based on education
            if 'EDUCATION' in l2_data:
                education = str(l2_data['EDUCATION']).lower()
                if 'college' in education or 'university' in education:
                    initial_goals.append("Use my education to make a meaningful impact")
                    initial_principles.append("Value knowledge and continuous learning")
        
        # Set the initial goals and principles
        self.reflection_memory.update_long_term_goals(initial_goals)
        self.reflection_memory.update_core_principles(initial_principles)

    def perceive(self, environment_state: Dict[str, Any] = None, social_context: Dict[str, Any] = None) -> List[str]:
        """
        Perceive the current environment and create memories.
        
        Args:
            environment_state (Dict): Current state of the environment
            social_context (Dict): Information about social interactions
            
        Returns:
            List[str]: List of observations made
        """
        observations = perceive_environment(
            agent=self,
            environment_state=environment_state,
            social_context=social_context
        )
        
        # Create memories for each observation
        for observation in observations:
            memory = create_memory_from_observation(
                agent=self,
                observation=observation,
                context="environmental_perception",
                source="observation"
            )
            self.memory_stream.add_memory(memory)
        
        return observations

    def retrieve(self, query_context: str, k: int = 10) -> List[MemoryRecord]:
        """
        Retrieve relevant memories based on context.
        
        Args:
            query_context (str): Context to search for
            k (int): Number of memories to retrieve
            
        Returns:
            List[MemoryRecord]: Relevant memories
        """
        return retrieve_relevant_memories(
            memory_store=self.memory_stream,
            query_context=query_context,
            k=k
        )

    def plan_day(self, target_date: datetime.date = None) -> Optional[Dict[str, Any]]:
        """
        Create a daily plan for the specified date.
        
        Args:
            target_date (datetime.date): Date to plan for
            
        Returns:
            Optional[Dict]: Daily plan with schedule and goals
        """
        daily_plan = create_daily_plan(
            agent=self,
            current_date=target_date
        )
        
        if daily_plan:
            # Create a memory of the planning activity
            planning_memory = create_memory_from_observation(
                agent=self,
                observation=f"I created a daily plan for {target_date or datetime.date.today()}",
                context="daily_planning",
                source="planning",
                manual_importance=7.0
            )
            self.memory_stream.add_memory(planning_memory)
            
            self.last_planning_time = datetime.datetime.now()
        
        return daily_plan

    def plan_week(self, week_start: datetime.date = None) -> Optional[Dict[str, Any]]:
        """
        Create a weekly plan.
        
        Args:
            week_start (datetime.date): Start date of the week
            
        Returns:
            Optional[Dict]: Weekly plan
        """
        weekly_plan = create_weekly_plan(
            agent=self,
            current_week_start=week_start
        )
        
        if weekly_plan:
            # Create a memory of the planning activity
            planning_memory = create_memory_from_observation(
                agent=self,
                observation=f"I created a weekly plan for the week starting {week_start or datetime.date.today()}",
                context="weekly_planning",
                source="planning",
                manual_importance=8.0
            )
            self.memory_stream.add_memory(planning_memory)
        
        return weekly_plan

    def plan_action(self, current_situation: str) -> Optional[str]:
        """
        Plan the next action based on current situation.
        
        Args:
            current_situation (str): Description of current situation
            
        Returns:
            Optional[str]: Planned action
        """
        return plan_next_action(
            agent=self,
            current_situation=current_situation
        )

    def execute(self, action: str, environment_state: Dict[str, Any] = None, social_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute an action and update internal state.
        
        Args:
            action (str): Action to execute
            environment_state (Dict): Current environment state
            social_context (Dict): Social context
            
        Returns:
            Dict: Execution result
        """
        return execute_action(
            agent=self,
            planned_action=action,
            environment_state=environment_state,
            social_context=social_context
        )

    def reflect(self, reflection_type: str = "daily") -> Optional[Any]:
        """
        Perform reflection on recent experiences.
        
        Args:
            reflection_type (str): Type of reflection ("daily", "weekly", etc.)
            
        Returns:
            Optional: Reflection record
        """
        if reflection_type == "daily":
            reflection = daily_reflection(agent=self)
        elif reflection_type == "insight":
            # Create insights from recent memories
            recent_memories = self.memory_stream.get_recent_memories(hours=48)
            if len(recent_memories) >= 5:
                reflection = create_insight(
                    agent=self,
                    related_memories=recent_memories[:5],
                    insight_context="Recent patterns and experiences"
                )
            else:
                reflection = None
        else:
            reflection = None
        
        if reflection:
            self.last_reflection_time = datetime.datetime.now()
        
        return reflection

    def step(self, environment_state: Dict[str, Any] = None, social_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform one cognitive step: perceive, retrieve, plan, execute, and potentially reflect.
        
        Args:
            environment_state (Dict): Current environment state
            social_context (Dict): Social context
            
        Returns:
            Dict: Results of the cognitive step
        """
        step_results = {
            'timestamp': datetime.datetime.now(),
            'observations': [],
            'planned_action': None,
            'execution_result': None,
            'reflection': None
        }
        
        # 1. Perceive the environment
        observations = self.perceive(environment_state, social_context)
        step_results['observations'] = observations
        
        # 2. Plan next action based on current situation
        current_situation = f"Currently at {self.current_location}. Recent observations: {'; '.join(observations[:3])}"
        planned_action = self.plan_action(current_situation)
        step_results['planned_action'] = planned_action
        
        # 3. Execute the planned action
        if planned_action:
            execution_result = self.execute(planned_action, environment_state, social_context)
            step_results['execution_result'] = execution_result
        
        # 4. Check if it's time for reflection (e.g., end of day)
        current_time = datetime.datetime.now()
        should_reflect = (
            self.last_reflection_time is None or 
            (current_time - self.last_reflection_time).total_seconds() > 86400  # 24 hours
        )
        
        if should_reflect:
            reflection = self.reflect("daily")
            step_results['reflection'] = reflection
        
        return step_results

    def get_status(self) -> Dict[str, Any]:
        """
        Get current status and statistics of the agent.
        
        Returns:
            Dict: Agent status information
        """
        memory_stats = self.memory_stream.get_statistics()
        reflection_stats = self.reflection_memory.get_statistics()
        
        status = {
            'id': self.id,
            'name': self.name,
            'current_location': self.current_location,
            'current_goal': self.current_goal,
            'mood': self.mood,
            'last_action': self.last_action,
            'last_action_time': self.last_action_time.isoformat() if self.last_action_time else None,
            'memory_statistics': memory_stats,
            'reflection_statistics': reflection_stats,
            'has_daily_plan': self.current_daily_plan is not None,
            'has_weekly_plan': self.current_weekly_plan is not None,
            'core_principles': self.reflection_memory.core_principles,
            'long_term_goals': self.reflection_memory.long_term_goals[:5]  # Show first 5 goals
        }
        
        return status

    def save_state(self, filepath: str) -> None:
        """
        Save the agent's complete state to files.
        
        Args:
            filepath (str): Base filepath for saving (without extension)
        """
        # Save memory stream
        self.memory_stream.save_to_file(f"{filepath}_memories.json")
        
        # Save reflection memory
        self.reflection_memory.save_to_file(f"{filepath}_reflections.json")
        
        # Save other state
        import json
        state_data = {
            'id': self.id,
            'name': self.name,
            'attributes': self.attributes,
            'abilities': self.abilities,
            'constraints': self.constraints,
            'current_location': self.current_location,
            'current_goal': self.current_goal,
            'current_planned_action': self.current_planned_action,
            'current_daily_plan': self.current_daily_plan,
            'current_weekly_plan': self.current_weekly_plan,
            'mood': self.mood,
            'last_reflection_time': self.last_reflection_time.isoformat() if self.last_reflection_time else None,
            'last_planning_time': self.last_planning_time.isoformat() if self.last_planning_time else None,
            'last_action_time': self.last_action_time.isoformat() if self.last_action_time else None,
            'last_action': self.last_action,
            'last_action_success': self.last_action_success
        }
        
        with open(f"{filepath}_state.json", 'w') as f:
            json.dump(state_data, f, indent=2)

    def load_state(self, filepath: str) -> None:
        """
        Load the agent's complete state from files.
        
        Args:
            filepath (str): Base filepath for loading (without extension)
        """
        import json
        
        # Load memory stream
        try:
            self.memory_stream.load_from_file(f"{filepath}_memories.json")
        except FileNotFoundError:
            print(f"Memory file not found: {filepath}_memories.json")
        
        # Load reflection memory
        try:
            self.reflection_memory.load_from_file(f"{filepath}_reflections.json", self.memory_stream)
        except FileNotFoundError:
            print(f"Reflection file not found: {filepath}_reflections.json")
        
        # Load other state
        try:
            with open(f"{filepath}_state.json", 'r') as f:
                state_data = json.load(f)
            
            self.current_location = state_data.get('current_location', 'unknown')
            self.current_goal = state_data.get('current_goal')
            self.current_planned_action = state_data.get('current_planned_action')
            self.current_daily_plan = state_data.get('current_daily_plan')
            self.current_weekly_plan = state_data.get('current_weekly_plan')
            self.mood = state_data.get('mood', 'neutral')
            self.last_action = state_data.get('last_action')
            self.last_action_success = state_data.get('last_action_success', True)
            
            # Parse datetime fields
            if state_data.get('last_reflection_time'):
                self.last_reflection_time = datetime.datetime.fromisoformat(state_data['last_reflection_time'])
            if state_data.get('last_planning_time'):
                self.last_planning_time = datetime.datetime.fromisoformat(state_data['last_planning_time'])
            if state_data.get('last_action_time'):
                self.last_action_time = datetime.datetime.fromisoformat(state_data['last_action_time'])
                
        except FileNotFoundError:
            print(f"State file not found: {filepath}_state.json")

    def __str__(self):
        """
        Return a comprehensive string representation of the agent.
        """
        
        # Basic info
        ret_string = f"CognitiveAgent(id={self.id}, name={self.name})"
        
        # Current state
        ret_string += f"\nCurrent Status:"
        ret_string += f"\n  Location: {self.current_location}"
        ret_string += f"\n  Mood: {self.mood}"
        ret_string += f"\n  Current Goal: {self.current_goal or 'None set'}"
        
        # Memory statistics
        memory_stats = self.memory_stream.get_statistics()
        ret_string += f"\nMemory: {memory_stats.get('total_memories', 0)} memories"
        
        # Reflection statistics
        reflection_stats = self.reflection_memory.get_statistics()
        ret_string += f"\nReflections: {reflection_stats.get('total_reflections', 0)} reflections"
        
        # Goals and principles
        if self.reflection_memory.long_term_goals:
            ret_string += f"\nTop Goals:"
            for i, goal in enumerate(self.reflection_memory.long_term_goals[:3], 1):
                ret_string += f"\n  {i}. {goal}"
        
        if self.reflection_memory.core_principles:
            ret_string += f"\nCore Principles:"
            for i, principle in enumerate(self.reflection_memory.core_principles[:3], 1):
                ret_string += f"\n  {i}. {principle}"
        
        # L2 data
        if self.l2_object:
            ret_string += f"\nL2_Data_Object: {str(self.l2_object)}"

        return ret_string
    

# Example instantiation and demonstration
if __name__ == "__main__":

    # import the necessary libraries
    import pandas as pd
    
    # load in l2 data from the example file
    l2_data = pd.read_csv('/Users/tristanbrigham/Desktop/Classes/Thesis/code_for_me/example_l2_data.txt', sep='\t')

    # for the first row of the l2 data, create an agent
    agent = Agent(id=1, l2_object=L2_Data_Object(l2_data.iloc[0]))

    # print the agent
    print("=== Initial Agent ===")
    print(agent)
    
    # Demonstrate cognitive capabilities
    print("\n=== Demonstrating Cognitive Capabilities ===")
    
    # 1. Environmental perception
    environment_state = {
        'location': 'home office',
        'time': datetime.datetime.now().strftime('%H:%M'),
        'weather': 'sunny',
        'objects': ['computer', 'desk', 'chair']
    }
    
    observations = agent.perceive(environment_state)
    print(f"\nObservations: {observations}")
    
    # 2. Daily planning
    daily_plan = agent.plan_day()
    print(f"\nDaily plan created: {daily_plan is not None}")
    if daily_plan:
        print(f"Main goals today: {daily_plan.get('main_goals_today', [])}")
    
    # 3. Action planning and execution
    current_situation = "I'm at my home office and need to be productive today"
    planned_action = agent.plan_action(current_situation)
    print(f"\nPlanned action: {planned_action}")
    
    if planned_action:
        execution_result = agent.execute(planned_action, environment_state)
        print(f"Execution successful: {execution_result['success']}")
    
    # 4. Reflection
    reflection = agent.reflect("daily")
    print(f"\nReflection created: {reflection is not None}")
    
    # 5. Show final status
    print("\n=== Final Agent Status ===")
    status = agent.get_status()
    print(f"Total memories: {status['memory_statistics']['total_memories']}")
    print(f"Total reflections: {status['reflection_statistics']['total_reflections']}")
    print(f"Current mood: {status['mood']}")
    print(f"Has daily plan: {status['has_daily_plan']}")