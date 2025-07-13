from tools.fallacy_detector_node import FallacyDetectorTool

if __name__ == "__main__":
    tool = FallacyDetectorTool()
    result = tool.invoke({"text": "You're wrong because you can't be trusted!"})
    print("Detected fallacies:", result["fallacies"])
