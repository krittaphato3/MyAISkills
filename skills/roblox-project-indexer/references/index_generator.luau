--!strict
-- roblox-project-indexer: index_generator.luau
-- Extracts comprehensive architecture data: scripts, networking remotes,
-- GUI surfaces, CollectionService tags, and place metadata.
-- Designed for execution via Studio MCP execute_luau in Edit mode.
-- Yields every 200 items to avoid freezing Studio or dropping MCP connections.

local HttpService = game:GetService("HttpService")
local CollectionService = game:GetService("CollectionService")

type ScriptInfo = {
	name: string,
	className: string,
	fullPath: string,
	parentPath: string,
	category: string,
	lineCount: number,
	runContext: string,
}

type RemoteInfo = {
	name: string,
	className: string,
	fullPath: string,
	parentPath: string,
	category: string,
}

type GuiInfo = {
	name: string,
	className: string,
	fullPath: string,
	parentPath: string,
	enabled: boolean,
	resetOnSpawn: boolean,
	viewportFramesCount: number,
}

type TagInfo = {
	tag: string,
	instanceCount: number,
	samplePaths: { string },
}

local TARGET_CONTAINERS: { { service: string, category: string } } = {
	{ service = "ServerScriptService", category = "Server" },
	{ service = "ReplicatedStorage", category = "Shared" },
	{ service = "StarterPlayer", category = "Client" },
	{ service = "StarterGui", category = "ClientUI" },
	{ service = "StarterPack", category = "ClientTools" },
	{ service = "ReplicatedFirst", category = "ClientFirst" },
	{ service = "ServerStorage", category = "ServerStorage" },
	{ service = "Workspace", category = "Workspace" },
	{ service = "Lighting", category = "Lighting" },
	{ service = "SoundService", category = "SoundService" },
	{ service = "MaterialService", category = "MaterialService" },
	{ service = "TextChatService", category = "Chat" },
}

local scriptsList: { ScriptInfo } = {}
local remotesList: { RemoteInfo } = {}
local guisList: { GuiInfo } = {}
local scanned = 0
local CHUNK_SIZE = 200

local scriptsByClass: { [string]: number } = {}
local remotesByClass: { [string]: number } = {}
local guisByClass: { [string]: number } = {}

local function getFullPath(inst: Instance): string
	local parts = { inst.Name }
	local cur = inst.Parent
	while cur and cur ~= game do
		table.insert(parts, 1, cur.Name)
		cur = cur.Parent
	end
	table.insert(parts, 1, "game")
	return table.concat(parts, ".")
end

local function getParentPath(inst: Instance): string
	local parent = inst.Parent
	if not parent then
		return "nil"
	end
	if parent == game then
		return "game"
	end
	return getFullPath(parent)
end

local function getRunContext(inst: Instance): string
	if inst:IsA("LocalScript") then
		return "Client"
	elseif inst:IsA("ModuleScript") then
		return "Module"
	elseif inst:IsA("Script") then
		local ok, rc = pcall(function()
			return (inst :: any).RunContext.Name
		end)
		if ok and rc then
			return rc
		end
		return "LegacyServer"
	end
	return "Unknown"
end

local function isNetworking(inst: Instance): boolean
	return inst:IsA("RemoteEvent")
		or inst:IsA("RemoteFunction")
		or inst:IsA("BindableEvent")
		or inst:IsA("BindableFunction")
		or inst:IsA("UnreliableRemoteEvent")
end

local function isGuiSurface(inst: Instance): boolean
	return inst:IsA("ScreenGui")
		or inst:IsA("BillboardGui")
		or inst:IsA("SurfaceGui")
end

local function scanContainer(root: Instance, category: string)
	local descendants: { Instance } = {}
	local ok, res = pcall(function()
		return root:GetDescendants()
	end)
	if ok and res then
		descendants = res
	else
		return
	end

	for _, inst in descendants do
		scanned += 1
		if scanned % CHUNK_SIZE == 0 then
			task.wait()
		end

		if inst:IsA("LuaSourceContainer") then
			local lineCount = 0
			local okSource, src = pcall(function()
				return (inst :: any).Source
			end)
			if okSource and typeof(src) == "string" and #src > 0 then
				local _, count = string.gsub(src, "\n", "")
				lineCount = count + 1
			end

			local className = inst.ClassName
			scriptsByClass[className] = (scriptsByClass[className] or 0) + 1

			table.insert(scriptsList, {
				name = inst.Name,
				className = className,
				fullPath = getFullPath(inst),
				parentPath = getParentPath(inst),
				category = category,
				lineCount = lineCount,
				runContext = getRunContext(inst),
			})
		elseif isNetworking(inst) then
			local className = inst.ClassName
			remotesByClass[className] = (remotesByClass[className] or 0) + 1

			table.insert(remotesList, {
				name = inst.Name,
				className = className,
				fullPath = getFullPath(inst),
				parentPath = getParentPath(inst),
				category = category,
			})
		elseif isGuiSurface(inst) then
			local className = inst.ClassName
			guisByClass[className] = (guisByClass[className] or 0) + 1

			local enabled = true
			local okEn, valEn = pcall(function()
				return (inst :: any).Enabled
			end)
			if okEn and typeof(valEn) == "boolean" then
				enabled = valEn
			end

			local resetOnSpawn = false
			local okRst, valRst = pcall(function()
				return (inst :: any).ResetOnSpawn
			end)
			if okRst and typeof(valRst) == "boolean" then
				resetOnSpawn = valRst
			end

			local vpCount = 0
			for _, child in inst:GetDescendants() do
				if child:IsA("ViewportFrame") then
					vpCount += 1
				end
			end

			table.insert(guisList, {
				name = inst.Name,
				className = className,
				fullPath = getFullPath(inst),
				parentPath = getParentPath(inst),
				enabled = enabled,
				resetOnSpawn = resetOnSpawn,
				viewportFramesCount = vpCount,
			})
		end
	end
end

-- Scan targeted containers
for _, entry in TARGET_CONTAINERS do
	local ok, container = pcall(function()
		return game:GetService(entry.service)
	end)
	if ok and container then
		scanContainer(container, entry.category)
	end
end

-- Scan CollectionService tags
local tagsList: { TagInfo } = {}
local okTags, allTags = pcall(function()
	return CollectionService:GetAllTags()
end)

if okTags and allTags then
	table.sort(allTags)
	for _, tag in allTags do
		local okInstances, taggedInstances = pcall(function()
			return CollectionService:GetTagged(tag)
		end)
		if okInstances and taggedInstances then
			local samplePaths: { string } = {}
			for i = 1, math.min(#taggedInstances, 5) do
				table.insert(samplePaths, getFullPath(taggedInstances[i]))
			end
			table.insert(tagsList, {
				tag = tag,
				instanceCount = #taggedInstances,
				samplePaths = samplePaths,
			})
		end
	end
end

local placeId = 0
pcall(function()
	placeId = game.PlaceId
end)

local gameId = 0
pcall(function()
	gameId = game.GameId
end)

local placeName = "Unknown"
pcall(function()
	placeName = game.Name
end)

local result = {
	placeInfo = {
		name = placeName,
		placeId = placeId,
		gameId = gameId,
		totalInstancesScanned = scanned,
		scannedAt = os.date("!%Y-%m-%dT%H:%M:%SZ"),
	},
	summary = {
		totalScripts = #scriptsList,
		scriptsByClass = scriptsByClass,
		totalRemotes = #remotesList,
		remotesByClass = remotesByClass,
		totalGuis = #guisList,
		guisByClass = guisByClass,
		totalTags = #tagsList,
	},
	scripts = scriptsList,
	networking = remotesList,
	guis = guisList,
	tags = tagsList,
}

return HttpService:JSONEncode(result)
