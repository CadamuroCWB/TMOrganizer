from rest_framework import serializers
from .models import Client, Contact


class ClientSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Client com validações personalizadas"""
    
    # Campos calculados
    full_address = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'alias', 'cnpj', 'email', 'phone', 'address',
            'start_date', 'tax_regime', 'legal_nature', 'end_consumer',
            'subject_protest', 'logo', 'logo_url', 'isic', 'home_directory',
            'full_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_address', 'logo_url']
    
    def get_full_address(self, obj):
        """Retorna endereço completo formatado"""
        if obj.address:
            return str(obj.address)
        return None
    
    def get_logo_url(self, obj):
        """Retorna URL da logo se existir"""
        if obj.logo:
            return obj.logo.url
        return None
    
    def validate_cnpj(self, value):
        """Validação personalizada de CNPJ"""
        if value and not self.instance:  # Apenas para criação
            if Client.objects.filter(cnpj=value).exists():
                raise serializers.ValidationError("CNPJ já cadastrado.")
        return value


class ClientListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de clientes"""
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'alias', 'cnpj', 'email', 'phone', 'end_consumer']


class ContactSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Contact"""
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_cpf(self, value):
        """Validação personalizada de CPF"""
        if value and not self.instance:  # Apenas para criação
            if Contact.objects.filter(cpf=value).exists():
                raise serializers.ValidationError("CPF já cadastrado.")
        return value