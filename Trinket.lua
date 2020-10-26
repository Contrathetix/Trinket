Trinket = {}

Trinket.Name = 'Trinket'
Trinket.GuildMemberList = {}
Trinket.GuildMemberList.Default = { Name = '', MemberCount = 0, MemberData = {} }
Trinket.GuildMemberList.Version = 1
Trinket.GuildMemberList.Data = nil

function Trinket.FormatDate(secondsAgo)

    local currentTime = os.time()
    local offsetSecondsFromUtc = 60 * 60 * 2
    local timeThen = currentTime - secondsAgo - offsetSecondsFromUtc
    return os.date('%Y-%m-%d %H:%M:%S', timeThen)

end

function Trinket.ExportGuildMemberList(args)

    d('Trinket: Export guild member list...')

    local options = {}
    local searchResult = { string.match(args, "^(%S*)%s*(.-)$") }

    for i,v in pairs(searchResult) do
        if (v ~= nil and v ~= "") then
            options[i] = string.lower(v)
        end
    end

    local guildId = GetGuildId(tonumber(options[1], 10))
    local guildSize = GetNumGuildMembers(guildId)

    Trinket.GuildMemberList.Data.Name = GetGuildName(guildId)
    Trinket.GuildMemberList.Data.MemberCount = guildSize
    Trinket.GuildMemberList.Data.MemberData = {}

    d('Trinket: Export for guild '..tostring(guildId)..' ('..GetGuildName(guildId)..', '..tostring(guildSize)..' members)')

    for memberIndex = 1, guildSize do
        local name, note, rankIndex, playerStatus, secsSinceLogoff = GetGuildMemberInfo(guildId, memberIndex)
        --d('Member: '..tostring(memberIndex)..' -> '..name)
        local rankName = GetGuildRankCustomName(guildId, rankIndex)
        table.insert(Trinket.GuildMemberList.Data.MemberData, {
            Name = name,
            Rank = rankName,
            LastOnlineUtc = Trinket.FormatDate(secsSinceLogoff),
            Note = note
        })
    end

    --d(Trinket.GuildMemberList.Data.MemberData)
    d('Trinket: Finished')

end

function Trinket.OnAddOnLoaded(_, addOnName)

    if addOnName == Trinket.Name then
        SLASH_COMMANDS['/guildexport'] = Trinket.ExportGuildMemberList
        Trinket.GuildMemberList.Data = ZO_SavedVars:NewAccountWide(
            'TrinketGuildMemberList',
            Trinket.GuildMemberList.Version,
            nil,
            Trinket.GuildMemberList.Default
        )
    end

end

EVENT_MANAGER:RegisterForEvent(Trinket.Name, EVENT_ADD_ON_LOADED, Trinket.OnAddOnLoaded)
