# Maximo-BeeAI-Agents
Working with BeeAI Agent to work with Maximo data using Bee-Stack

GenAI is revolutionizing the world, transitioning from concept to reality, with hashtag#AIAgents leading the way ☘️ 
❓ Can we use AI Agents with Maximo? 
❓ Can they help our users in there day to day tasks 🤔

This [video](https://www.youtube.com/watch?v=rrgGYyaANbI) unveils the potential, showcasing an 𝐀𝐈 𝐀𝐠𝐞𝐧𝐭 🤖 as a Smart Assistant for Maintenance Personnel using 𝐈𝐁𝐌 𝐌𝐚𝐱𝐢𝐦𝐨 ☀️ 


## 🌀𝐂𝐨𝐦𝐩𝐨𝐧𝐞𝐧𝐭𝐬 :
 - 🔺IBM Granite-3B LLM
 - 🔺IBM Watsonx.ai
 - 🔺BeeAI-Framework 🐝 - Bee-Stack
 - 🔺IBM Maximo Application Suite

 
## How to Setup/Run:

### Setup Podman
If running in Podman, then machine should have root privilege. To Setup Podman Machine-

podman machine init
podman machine set --rootful=true
podman machine Start
podman machine list  #Verify the machine is running and set as default

### Clone Bee-Stack
git clone https://github.com/i-am-bee/bee-stack.git
cd bee-stack
Start Bee-Stack- ./bee-stack.sh start --runtime=podman
Stop Bee-Stack- ./bee-stack.sh stop --runtime=podman
Clean Bee-Stack- ./bee-stack.sh clea  --runtime=podman


