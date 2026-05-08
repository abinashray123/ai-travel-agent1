import time
from langchain_core.messages import HumanMessage, AIMessage
from src.agents.travel_agent import agent
from src.utils.logger import get_logger
from src.utils.custom_exception import CustomException

logger = get_logger(__name__)

class TravelPlanner:
    def __init__(self):
        self.messages = []
        logger.info("TravelPlanner initialized")

    def create_itinerary(
        self,
        city: str,
        days: int,
        interests: list[str],
        style: str,
        pace: str,
        month: str | None = None,
        max_retries: int = 3
    ):
        try:
            user_prompt = f"""
            Plan a {days}-day trip to {city}

            Interests: {', '.join(interests)}
            Travel Style: {style}
            Pace: {pace}
            Month: {month or 'Any'}

            Provide a detailed itinerary.
            """

            self.messages.append(HumanMessage(content=user_prompt))

            # Retry logic with exponential backoff
            for attempt in range(max_retries):
                try:
                    logger.info(f"Invoke attempt {attempt + 1}/{max_retries}")
                    response = agent.invoke({
                        "messages": self.messages
                    })

                    final_answer = response["messages"][-1].content
                    self.messages.append(AIMessage(content=final_answer))

                    return final_answer

                except Exception as e:
                    error_msg = str(e)
                    is_connection_error = any(keyword in error_msg.lower() for keyword in 
                                             ["connection", "timeout", "getaddrinfo", "network", "unreachable"])
                    
                    if is_connection_error and attempt < max_retries - 1:
                        wait_time = (2 ** attempt) + (attempt * 0.5)
                        logger.warning(f"Connection error (attempt {attempt + 1}): {error_msg}")
                        logger.info(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        raise

        except Exception as e:
            logger.error(f"Planner error: {e}")
            raise CustomException("Failed to generate itinerary", e)
