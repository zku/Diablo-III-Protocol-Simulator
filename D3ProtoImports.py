#! /usr/bin/env python

# this is an incredibly ugly hack - stupid python imports.. wtb #include <herpderp.hpp>

try:
  import sys
  sys.path.append('./libs/')
  sys.path.append('./libs/services/')
  sys.path.append('./libs/proto/')
  sys.path.append('./libs/proto/lib/')
  sys.path.append('./libs/proto/service/')
  sys.path.append('./libs/proto/google/')
  try:
    import proto.Account_pb2 as Account
  except:
    pass
  try:
    import proto.AttributeSerializer_pb2 as AttributeSerializer
  except:
    pass
  try:
    import proto.GameMessage_pb2 as GameMessage
  except:
    pass
  try:
    import proto.GBHandle_pb2 as GBHandle
  except:
    pass
  try:
    import proto.Hero_pb2 as Hero
  except:
    pass
  try:
    import proto.Hireling_pb2 as Hireling
  except:
    pass
  try:
    import proto.ItemCrafting_pb2 as ItemCrafting
  except:
    pass
  try:
    import proto.Items_pb2 as Items
  except:
    pass
  try:
    import proto.lib.config.process_config_pb2 as process_config
  except:
    pass
  try:
    import proto.lib.profanity.profanity_pb2 as profanity
  except:
    pass
  try:
    import proto.lib.protocol.attribute_pb2 as attribute
  except:
    pass
  try:
    import proto.lib.protocol.content_handle_pb2 as content_handle
  except:
    pass
  try:
    import proto.lib.protocol.descriptor_pb2 as descriptor
  except:
    pass
  try:
    import proto.lib.protocol.entity_pb2 as entity
  except:
    pass
  try:
    import proto.lib.protocol.exchange_object_provider_pb2 as exchange_object_provider
  except:
    pass
  try:
    import proto.lib.protocol.exchange_pb2 as exchange
  except:
    pass
  try:
    import proto.lib.protocol.invitation_pb2 as invitation
  except:
    pass
  try:
    import proto.lib.protocol.resource_pb2 as resource
  except:
    pass
  try:
    import proto.lib.rpc.connection_pb2 as connection
  except:
    pass
  try:
    import proto.OnlineService_pb2 as OnlineService
  except:
    pass
  try:
    import proto.PartyMessage_pb2 as PartyMessage
  except:
    pass
  try:
    import proto.Quest_pb2 as Quest
  except:
    pass
  try:
    import proto.service.authentication.authentication_pb2 as authentication
  except:
    pass
  try:
    import proto.service.channel.channel_types_pb2 as channel_types
  except:
    pass
  try:
    import proto.service.channel.definition.channel_pb2 as channel
  except:
    pass
  try:
    import proto.service.channel_invitation.definition.channel_invitation_pb2 as channel_invitation
  except:
    pass
  try:
    import proto.service.exchange.exchange_pb2 as exchange
  except:
    pass
  try:
    import proto.service.exchange.exchange_types_pb2 as exchange_types
  except:
    pass
  try:
    import proto.service.followers.definition.followers_pb2 as followers
  except:
    pass
  try:
    import proto.service.friends.definition.friends_pb2 as friends
  except:
    pass
  try:
    import proto.service.friends.friends_types_pb2 as friends_types
  except:
    pass
  try:
    import proto.service.game_master.game_factory_pb2 as game_factory
  except:
    pass
  try:
    import proto.service.game_master.game_master_pb2 as game_master
  except:
    pass
  try:
    import proto.service.game_master.game_master_types_pb2 as game_master_types
  except:
    pass
  try:
    import proto.service.game_utilities.game_utilities_pb2 as game_utilities
  except:
    pass
  try:
    import proto.service.notification.notification_pb2 as notification
  except:
    pass
  try:
    import proto.service.presence.presence_pb2 as presence
  except:
    pass
  try:
    import proto.service.presence.presence_types_pb2 as presence_types
  except:
    pass
  try:
    import proto.service.search.search_pb2 as search
  except:
    pass
  try:
    import proto.service.search.search_types_pb2 as search_types
  except:
    pass
  try:
    import proto.service.server_pool.server_pool_pb2 as server_pool
  except:
    pass
  try:
    import proto.service.storage.storage_pb2 as storage
  except:
    pass
  try:
    import proto.service.toon.toon_external_pb2 as toon_external
  except:
    pass
  try:
    import proto.service.toon.toon_pb2 as toon
  except:
    pass
  try:
    import proto.service.user_manager.user_manager_pb2 as user_manager
  except:
    pass
  try:
    import proto.Settings_pb2 as Settings
  except:
    pass
  try:
    import proto.Stats_pb2 as Stats
  except:
    pass
except:
  pass
  