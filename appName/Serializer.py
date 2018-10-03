import traceback

from django.contrib.auth.models import User
from django.db.models import F
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from models import Building, Towns, Profile, Troop
import ast


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'profile')


class TroopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Troop
        fields = ('id', 'type', 'tier', 'town', 'img', 'created_date', 'change_date', 'preparation_time', 'status',
                  'power', 'town_position', 'cost',)

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        if instance.status != "preparing" and validated_data["status"] == "preparing":
            if ((instance.cost["stone"] > instance.town.resources["stone"]) if ("stone" in instance.cost) else False) or ((instance.cost["wood"] > instance.town.resources["wood"]) if ("wood" in instance.cost) else False) or ((instance.cost["food"] > instance.town.resources["food"]) if ("food" in instance.cost) else False):
                raise ValueError("Not enough resources for troop update")
            else:
                troop_town = Towns.objects.filter(id=validated_data["town"].id)
                if troop_town.get().troop_queue < troop_town.get().military_process_limit: # hersey uygun level up icin
                    troop_town.update(troop_queue=F('troop_queue') + 1,
                                      resources={"wood": (troop_town.get().resources["wood"]) - ((instance.cost["wood"]) if ("wood" in instance.cost) else 0),
                                                 "food": (troop_town.get().resources["food"]) - ((instance.cost["food"]) if ("food" in instance.cost) else 0),
                                                 "stone": (troop_town.get().resources["stone"]) - ((instance.cost["stone"]) if ("stone" in instance.cost) else 0)})
                else:
                    raise ValueError("Your troop process limit is at maximum")

        if instance.status != "ready" and validated_data["status"] == "ready":
            troop_town = Towns.objects.filter(id=validated_data["town"].id)
            Towns.objects.filter(id=validated_data["town"].id).update(troop_queue=F('troop_queue') - 1,
                                                                      resources={"wood": (troop_town.get().resources["wood"]) + (instance.cost["wood"] if ("wood" in instance.cost) else 0),
                                                                              "food": (troop_town.get().resources["food"]) + (instance.cost["food"] if ("food" in instance.cost) else 0),
                                                                              "stone": (troop_town.get().resources["stone"]) + (instance.cost["stone"] if ("stone" in instance.cost) else 0)})


        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

            return ExampleModel.objects.create(**validated_data)

        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:

            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance

        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            if validated_data["status"] == "preparing":
                troop_cost = Troop.objects.filter(type=validated_data["type"]).first().cost
                if (((troop_cost["stone"] > validated_data["town"].resources["stone"]) if ("stone" in troop_cost) else False) or
                    ((troop_cost["food"] > validated_data["town"].resources["food"]) if ("food" in troop_cost) else False) or
                    ((troop_cost["wood"] > validated_data["town"].resources["wood"]) if ("wood" in troop_cost) else False)):
                    raise ValueError("Not enough resources for create this troop")
                elif validated_data["town"].population < validated_data["town"].population_limit:
                    troop_town = Towns.objects.filter(id=validated_data["town"].id)
                    if troop_town.get().troop_queue < troop_town.get().military_process_limit:  # hersey uygun level up icin
                        troop_town.update(troop_queue=F('troop_queue') + 1,
                                          resources={"wood": (troop_town.get().resources["wood"]) - ((troop_cost["wood"]) if ("wood" in troop_cost) else 0),
                                                     "food": (troop_town.get().resources["food"]) - ((troop_cost["food"]) if ("food" in troop_cost) else 0),
                                                     "stone": (troop_town.get().resources["stone"]) - ((troop_cost["stone"]) if ("stone" in troop_cost) else 0)})
                    else:
                        raise ValueError("Your troop process limit is at maximum")
                else:
                    raise ValueError("Population is at maximum")

            instance = ModelClass.objects.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = ('id', 'type', 'level', 'town', 'img', 'created_date', 'change_date', 'construction_time', 'status', 'cost', 'sector', 'special')

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        if instance.status != "loading" and validated_data["status"] == "loading":
            if ((instance.cost["stone"] > instance.town.resources["stone"]) if ("stone" in instance.cost) else False) or ((instance.cost["wood"] > instance.town.resources["wood"]) if ("wood" in instance.cost) else False) or ((instance.cost["food"] > instance.town.resources["food"]) if ("food" in instance.cost) else False):
                raise ValueError("Not enough resources")
            else:
                buildings_town = Towns.objects.filter(id=validated_data["town"].id)
                if buildings_town.get().building_queue < buildings_town.get().building_process_limit:
                    buildings_town.update(building_queue=F('building_queue')+1,
                                          resources={"wood": (buildings_town.get().resources["wood"]) - (instance.cost["wood"] if ("wood" in instance.cost) else 0),
                                                     "food": (buildings_town.get().resources["food"]) - (instance.cost["food"] if ("food" in instance.cost) else 0),
                                                     "stone": (buildings_town.get().resources["stone"]) - (instance.cost["stone"] if ("stone" in instance.cost) else 0)})
                else:
                    raise ValueError("Your building process limit is maximum")

        if instance.status != "completed" and validated_data["status"] == "completed":
            buildings_town = Towns.objects.filter(id=validated_data["town"].id)
            Towns.objects.filter(id=validated_data["town"].id).update(building_queue=F('building_queue')-1,
                                                                      resources={"wood": (buildings_town.get().resources["wood"]) + (instance.cost["wood"] if ("wood" in instance.cost) else 0),
                                                                              "food": (buildings_town.get().resources["food"]) + (instance.cost["food"] if ("food" in instance.cost) else 0),
                                                                              "stone": (buildings_town.get().resources["stone"]) + (instance.cost["stone"] if ("stone" in instance.cost) else 0)})

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance


class ReadOnlyTownSerializer(serializers.ModelSerializer):

    buildings = BuildingSerializer(many=True, read_only=True)
    troops = TroopSerializer(many=True, read_only=True)

    class Meta:
        model = Towns
        fields = ('id', 'name', 'military', 'buildings', 'whom', 'resources', 'troops', 'building_queue', 'troop_queue', 'building_process_limit', 'military_process_limit', 'x_coord', 'y_coord', 'population_limit', 'population', 'production')


class CreateUpdateTownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Towns
        fields = ('id', 'name', 'military', 'whom', 'resources', 'building_queue', 'troop_queue', 'military_process_limit', 'building_process_limit', 'x_coord', 'y_coord')

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr == "resources":
                value = ast.literal_eval(value)
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

    def create(self, validated_data):
        if "resources" in validated_data:
            validated_data["resources"] = ast.literal_eval(validated_data["resources"])

        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass.objects.create(**validated_data)
            types1 = ['main', 'timber', 'stone']
            types0 = ["farm", 'depot', 'barrack', 'stable', 'archery', 'house', 'shelter', 'workshop', 'wall']

            for i in types1:
                Building.objects.create(type=i, level=1, town=instance, status='completed')
            for i in types0:
                Building.objects.create(type=i, level=0, town=instance, status='completed')
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class ReadOnlyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    town = ReadOnlyTownSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ("bio", 'user', 'score', 'town')


class CreateUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'user', 'town')




