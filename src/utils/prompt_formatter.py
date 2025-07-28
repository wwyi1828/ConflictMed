# Updated to include the robust DPOPrompter
"""
A dedicated helper to manage templates and prompt building.
"""

import json
import os.path as osp
from typing import Union, Dict, Any

class DPOPrompter(object):
    __slots__ = ("template", "_verbose")
    
    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
        if not template_name:
            # Enforce the default here, so the constructor can be called with '' and will not break.
            template_name = "dpo_template"
        file_name = osp.join("templates", f"{template_name}.json")
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )
    
    def generate_prompt(
        self,
        prompt: str,
        chosen: Union[None, str] = None,
        rejected: Union[None, str] = None,
    ) -> Dict[str, Any]:
        """
        Generate formatted examples for DPO training
        
        Args:
            prompt: The input prompt/question
            chosen: The preferred response (optional)
            rejected: The non-preferred response (optional)
            
        Returns:
            Dictionary containing the formatted prompt and responses
        """
        # Format the input according to the template
        formatted_prompt = self.template["prompt_format"].format(prompt=prompt)
        
        result = {
            "prompt": formatted_prompt,
        }
        
        # Add chosen and rejected responses if provided
        if chosen:
            result["chosen"] = chosen
        
        if rejected:
            result["rejected"] = rejected
            
        if self._verbose:
            print(f"Formatted prompt: {formatted_prompt}")
            if chosen:
                print(f"Chosen response: {chosen}")
            if rejected:
                print(f"Rejected response: {rejected}")
                
        return result
    
    def process_dataset_item(self, data_point: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a dataset item into the format expected by DPO trainer
        
        Args:
            data_point: A dictionary containing dataset fields
            
        Returns:
            Dictionary formatted for DPO training
        """
        # Extract fields based on dataset structure
        # This handles different possible field names
        prompt = data_point.get("prompt", data_point.get("input", data_point.get("question", "")))
        chosen = data_point.get("chosen", data_point.get("preferred", data_point.get("positive", "")))
        rejected = data_point.get("rejected", data_point.get("dispreferred", data_point.get("negative", "")))
        
        # Generate the formatted prompt and responses
        return self.generate_prompt(prompt, chosen, rejected)
    
    def get_response(self, output: str) -> str:
        """Extract the response from model output"""
        if "response_split" in self.template:
            return output.split(self.template["response_split"])[1].strip()
        return output